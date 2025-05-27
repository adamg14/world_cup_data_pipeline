import kagglehub
import shutil
import pandas as pd
import os
from adlfs import AzureBlobFileSystem
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

account_name = os.getenv("STORAGE_ACCOUNT_NAME")
account_key = os.getenv("STORAGE_ACCOUNT_KEY")

# azure data lake file system
fs = AzureBlobFileSystem(
    account_name=account_name,
    account_key=account_key
)

def get_azure_fs():
    return AzureBlobFileSystem(
    account_name=os.getenv("STORAGE_ACCOUNT_NAME"),
    account_key=os.getenv("STORAGE_ACCOUNT_KEY"),
)

def extract_dataset(url, destination_directory):
    source_directory = kagglehub.dataset_download(url)


    for filename in os.listdir(source_directory):
        if filename.endswith('.csv'):

            source_path = os.path.join(source_directory, filename)
            destination_path = os.path.join(destination_directory, filename)

            shutil.copy2(source_path, destination_path)


    df = pd.read_csv(destination_path)

    return df


def read_csv(file_path):
    return pd.read_csv(file_path)


def write_data_lake(local_file_path, adl_file_path):
    fs = get_azure_fs()
    with open(local_file_path, "rb") as data_source:
        with fs.open(adl_file_path, 'wb') as data_lake:
            data_lake.write(data_source.read())

# write_data_lake("data/stadiums.csv", "/raw-data/stadiums.csv")