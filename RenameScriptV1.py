# ---------------------------------
# Created by: Nico Saboonchi
# File Name: Rename Script.py
# Date: 9/6/2024
# Function: This script will take a fulcrum CSV and rename all the downloaded photos with columns from the csv file
#           place them into a new directory.
# ---------------------------------

import os
import csv
import shutil
import time
from tkinter import *
from tkinter import ttk

# Create a decorator to time the functions
def timer(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function(*args, **kwargs)
        end_time = time.time()
        print(f"Took {end_time - start_time} seconds")

    return wrapper


@timer
def fm_image_rename(csv_file, source_dir, new_dir):
    os.makedirs(new_dir, exist_ok=True)

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

        for row in rows:
            new_name = row["no column"]
            org_name = row["photos"].split(",")

            for idx, img in enumerate(org_name):
                org_file_path = os.path.join(source_dir, img + ".jpg")
                new_file_name = f"{new_name} - {idx + 1}.jpg"
                new_file_path = os.path.join(new_dir, new_file_name)

                if os.path.exists(new_file_path):
                    print(f"{new_file_name} already exists, skipping file")
                    pass
                else:
                    try:
                        shutil.copy(org_file_path, new_file_path)
                        print(f" Successfully renamed {img} to {new_file_name}")
                    except FileNotFoundError:
                        print(f"{org_name} file not found")


if __name__ == "__main__":
    print("Hello :) this script will take in an asset CSV from fulcrum and using the columns\n"
          "in the CSV rename the photos to a new name and store them to a different directory")

    csv_file = r"C:\Users\nico.saboo\Documents\Golden One\g1c_asset_data\g1c_asset_data.csv"
    source_dir = r'C:\Users\nico.saboo\Documents\Golden One\g1c_asset_data'
    new_dir = r'C:\Users\nico.saboo\Documents\Golden One\Renamed'

    # csv_file = input("Enter the path to the csv file: ")
    # input_column = input("Specify the column which you want the photos to be renamed to: ")
    # photos_column = input("Specify the column which the photos are listed in: ")
    # source_dir = input("Enter the path to where the unnamed photos are: ")
    # new_dir = input("Enter the path to where you want the renamed photos to transfer to: ")

    # # csv_file = r"C:\Users\nico.saboo\Downloads\Fulcrum_Export_060d8037-6fd5-484d-9852-e60401dc0f13\avondale_fca_arch\avondale_fca_arch.csv"
    # # source_dir = r"C:\Users\nico.saboo\Downloads\Fulcrum_Export_060d8037-6fd5-484d-9852-e60401dc0f13\avondale_fca_arch"
    # # new_dir = r'C:\Users\nico.saboo\Documents\Avondale Renamed'

    fm_image_rename(csv_file, source_dir, new_dir)
