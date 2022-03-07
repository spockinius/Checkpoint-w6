# Import needed modules
import requests
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobClient
import os

# Define credentials
credential = AzureCliCredential()
subscription_id = os.environ["SUBSCRIPTION_ID"]
resource_client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)

# Function to write names to a file
def kirjoitanimet():
    tiedosto = requests.get("https://2ri98gd9i4.execute-api.us-east-1.amazonaws.com/dev/academy-checkpoint2-json")
    data = tiedosto.json()
    with open("checkpoint.txt", "w") as f:
        for i in data["items"]:
            f.write(i["parameter"] + "\n")

# Function to create a new resource group where you can insert new storage account and blob container
def newrg(name: str, location: str):
    rg_result = resource_client.resource_groups.create_or_update(
        name,
        {
            "location": location
        }
    )
    print(f"Resource group named {rg_result.name} has been created in the {rg_result.location} region")

# Function to create a new storage account
def newstorage(rgname: str, storagename: str, location: str):
    storage_client.storage_accounts.begin_create(
        rgname,
        storagename,
        {
          "sku": {
            "name": "Standard_GRS"
          },
          "kind": "StorageV2",
          "location": location,
          "encryption": {
            "services": {
              "file": {
                "key_type": "Account",
                "enabled": True
              },
              "blob": {
                "key_type": "Account",
                "enabled": True
              }
            },
            "key_source": "Microsoft.Storage"
          },
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
    ).result()
    print(f"New storage account named {storagename} created in resourcegroup {rgname}, in location {location}")

# Function to create new blob container
def createblob(rgname: str, storagename: str, blobname: str):
    blob_container = storage_client.blob_containers.create(
        rgname,
        storagename,
        blobname,
        {}
    )
    print(f"Created blob container named {blobname} into resourcegroup {rgname} under storage account {storagename}")     

# Function to upload document to a blob container, container string must be obtained from Azure portal
def uploadblob(connectionstring: str, filename: str, container: str, blobname: str):
    blob = BlobClient.from_connection_string(conn_str=connectionstring, container_name=container, blob_name=blobname)

    with open(filename, "rb") as f:
      blob.upload_blob(f)
    
    print(f"File {filename} has been uploaded to blob container {blobname}")

# Call functions here
if __name__ == "__main__":
    uploadblob(<string>, "testi.txt", "katablobtentti", "testi.txt")            
