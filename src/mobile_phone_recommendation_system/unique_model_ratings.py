"""
Module to rate the unique models based on their popularity
"""

import ast
import contextlib
import io
import json
import os

from .ai_response_generator import AIResponseGenerator
from .data_cleaner import DataCleaner


class RateUniqueModels:
    """Class to rate the unique models based on their performace"""

    def __init__(self):
        """Constructor of the RateUniqueModels class"""

        # Variable to store the unique models list fetched from the CSV file
        self._unique_models_list_fetched_from_csv = {}

        # Variable to store the length of the unique models list fetched from the CSV file
        self._length_of_unique_models_list_fetched_from_csv = None

        # Variable to store the length of the rated unique models dictionary fetched from the AI
        self._length_of_rated_unique_models_dictionary_fetched_from_ai = None

        # Variable to store the rated unique models dictionary fetched from the AI
        self._rated_unique_models_dictionary_from_ai = {}

        # Variable to store the file path where the ratings JSON file of the models will be stored
        self._file_path_to_store_ratings = os.path.join(
            os.path.dirname(__file__),
            "ratings_files",
            "model_ratings.json",
        )

    def generate_ratings(self):
        """Method to generate the ratings for each models using AI"""

        # Fetch the unique models list from CSV
        data_cleaner = DataCleaner()
        self._unique_models_list_fetched_from_csv = (
            data_cleaner.get_list_of_unique_models()
        )

        # Fetch the instructions file and its contents
        instruction_dir = os.path.join(os.path.dirname(__file__), "instructions")
        instructions = None

        with open(
            os.path.join(instruction_dir, "instructions_to_rank_unique_models.txt")
        ) as instructions_file:
            instructions = instructions_file.read()

        # Get the length of the unique models list from CSV
        self._length_of_unique_models_list_fetched_from_csv = len(
            self._unique_models_list_fetched_from_csv
        )

        # Since AI can make mistakes and omit out models on its own, we run the loop until the length of unique models from CSV matches the lenth of unique models from AI
        while (
            self._length_of_unique_models_list_fetched_from_csv
            != self._length_of_rated_unique_models_dictionary_fetched_from_ai
        ):
            starting_index = 0
            while (
                starting_index
            ) < self._length_of_unique_models_list_fetched_from_csv:
                ending_index = starting_index + 10
                if ending_index > self._length_of_unique_models_list_fetched_from_csv:
                    ending_index = self._length_of_unique_models_list_fetched_from_csv
                sliced_dictionary = {}
                for i in range(starting_index, ending_index):
                    sliced_dictionary[i - starting_index] = (
                        self._unique_models_list_fetched_from_csv[i]
                    )

                ai = AIResponseGenerator(
                    instructions=instructions,
                    question=f"The dictionary of model is {sliced_dictionary}. Arrange them as per the instructions.",
                )

                captured_output = io.StringIO()
                with contextlib.redirect_stdout(captured_output):
                    ai.get_answer()

                sorted_unique_models_dictionary_fetched_from_ai = ast.literal_eval(
                    captured_output.getvalue()
                )
                for i in range(starting_index, ending_index):
                    self._rated_unique_models_dictionary_from_ai[
                        sliced_dictionary[i - starting_index]
                    ] = sorted_unique_models_dictionary_fetched_from_ai[
                        i - starting_index
                    ]
                self._length_of_rated_unique_models_dictionary_fetched_from_ai = len(
                    self._rated_unique_models_dictionary_from_ai
                )
                print(
                    f"Rating all the available unique models. {int(self._length_of_rated_unique_models_dictionary_fetched_from_ai/self._length_of_unique_models_list_fetched_from_csv*100)} % completed. Please wait..."
                )
                starting_index = ending_index

        # Storing the rated unique models dictionary fetched from the AI in a JSON file
        with open(self._file_path_to_store_ratings, "w") as file_to_store_ratings:
            json.dump(
                self._rated_unique_models_dictionary_from_ai,
                file_to_store_ratings,
                indent=4,
            )
