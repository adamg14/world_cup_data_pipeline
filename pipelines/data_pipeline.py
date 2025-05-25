import kagglehub
import shutil
import pandas as pd
import os


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

print(extract_dataset("swaptr/fifa-world-cup-2022-statistics", "../data"))

print(read_csv("data/goalscorers.csv"))