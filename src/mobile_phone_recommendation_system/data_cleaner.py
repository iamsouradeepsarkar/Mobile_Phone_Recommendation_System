"""
Module to clean up the Mobile Data set.
Takes the MobileDataSet.csv file in the Mobile_data sub-directory as an input.
"""

import os
from pathlib import Path

import pandas as pd


class DataCleaner:
    """Class to clean up the Mobile Data csv file"""

    def __init__(self):
        """Constructor of the DataCleaner class"""

        # Path of the MobileDataSet.csv file
        self._csv_file_path = os.path.join(
            os.path.dirname(__file__), "Mobile_Data", "MobileDataSet.csv"
        )

        # Create the directory where the the refined CSV file will be stored
        directory_path = Path(
            os.path.join(os.path.dirname(__file__), "refined_mobile_data"),
            exist_ok=True,
        )
        directory_path.mkdir(exist_ok=True)

        # Path where the refined CSV file will be stored
        self._refined_csv_file_path = os.path.join(
            directory_path, "RefinedMobileDataSet.csv"
        )

        # Variables to store the relevant data
        self._processors_list = None
        self._companies_list = None
        self._models_name = None

        # Variable to store the Data Frame
        self._original_csv = None

        # Extracting the data Frame from the CSV
        try:
            self._original_csv = pd.read_csv(self._csv_file_path, encoding="cp1252")
        except FileNotFoundError as filenotfound:
            print(f"File: {self._csv_file_path} is not found. Error: {filenotfound}")
        except Exception as error:
            print(
                f"Couldn't extract data from the {self._csv_file_path} file. Error: {error}"
            )

    def refine_existing_data(self):
        """Method to refine the existing data and extract required information out of it"""

        # Dropping some columns as they aren't required
        self._original_csv = self._original_csv.drop(
            [
                "Launched Price (Pakistan)",
                "Launched Price (China)",
                "Launched Price (USA)",
                "Launched Price (Dubai)",
            ],
            axis=1,
        )

        # Refining the data
        self._original_csv["Storage"] = pd.to_numeric(
            self._original_csv["Model Name"]
            .str.split()
            .str[-1]
            .astype(str)
            .str.replace(r"[^\d]+", "", regex=True),
            errors="coerce",
        ).astype("Int64")
        self._original_csv["Model"] = (
            self._original_csv["Model Name"].str.rsplit(" ", n=1).str[0]
        )
        self._original_csv["Mobile Weight"] = self._original_csv["Mobile Weight"].str[
            0:-1
        ]
        self._original_csv["RAM"] = pd.to_numeric(
            self._original_csv["RAM"]
            .astype(str)
            .str.replace(r"[^\d\.]+", "", regex=True),
            errors="coerce",
        )
        self._original_csv["Front Camera"] = pd.to_numeric(
            self._original_csv["Front Camera"].str.split(" ").str[0].str[0:-2],
            errors="coerce",
        )
        self._original_csv["Back Camera"] = pd.to_numeric(
            self._original_csv["Back Camera"].str.split(" ").str[0].str[0:-2],
            errors="coerce",
        )
        self._original_csv["Screen Size"] = (
            self._original_csv["Screen Size"].str.split(" ").str[0]
        )
        self._original_csv["Battery Capacity"] = (
            self._original_csv["Battery Capacity"]
            .str[0:-3]
            .str.replace(",", "")
            .astype(int)
        )
        self._original_csv["Launched Price (India)"] = (
            self._original_csv["Launched Price (India)"].str.split(" ").str[1]
        )
        self._original_csv["Launched Price (India)"] = (
            self._original_csv["Launched Price (India)"]
            .str.replace(",", "")
            .astype(int)
        )

        self._original_csv.to_csv(self._refined_csv_file_path)

    def get_list_of_unique_processors(self):
        """Method to get the list of all unique processors"""
        self._processors_list = self._original_csv["Processor"].unique().tolist()
        return self._processors_list

    def get_list_of_unique_companies(self):
        """Method to get the list of all unique companies"""
        self._companies_list = self._original_csv["Company Name"].unique().tolist()
        return self._companies_list

    def get_list_of_unique_models(self):
        """Method to get the list of all unique models"""
        refined_csv_file_data = pd.read_csv(self._refined_csv_file_path)
        self._models_name = refined_csv_file_data["Model"].unique().tolist()
        return self._models_name
