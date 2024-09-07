import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

LOCAL_DB_PATH = "flashcards.db"
AZURE_BLOB_CONNECTION_STRING = os.getenv("azure_blob_connection_string")
AZURE_BLOB_CONTAINER_NAME = os.getenv("azure_blob_container_name")
AZURE_BLOB_DB_NAME = os.getenv("azure_blob_db_name")


def sync_db_to_azure():
    """
    Sync the local SQLite database to Azure Blob Storage.

    :param local_db_path: Path to the local SQLite database file
    :param connection_string: Azure Storage account connection string
    :param container_name: Name of the container in Azure Blob Storage
    :param blob_name: Name to give the blob in Azure Storage
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION_STRING)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=AZURE_BLOB_CONTAINER_NAME, blob=AZURE_BLOB_DB_NAME)

        # Upload the file
        with open(LOCAL_DB_PATH, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    except Exception as e:
        print(e)
        raise


# Example usage
if __name__ == "__main__":
    sync_db_to_azure()
