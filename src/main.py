"""
Main module
"""

import ast
import contextlib
import io
import os
from pathlib import Path

from ai_response_generator import AIResponseGenerator
from data_cleaner import DataCleaner
from filter_mobiles_based_on_user_inputs import FilterMobilesBasedOnUserInputs
from unique_company_ratings import RateUniqueCompanies
from unique_model_ratings import RateUniqueModels
from unique_processor_ratings import RateUniqueProcessors


class MobileRecommender:
    """Class to recommend mobile phones based on user inputs"""

    def __init__(self):
        """Constructor of the MobileRecommender class"""

        # Variable to store the user prompt
        self._user_prompt = None

        # Path to the directory where the instructions for the AI are stored
        self._ai_instructions_directory = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "instructions"
        )

        # Variable to store the dictionary of requirements extracted from the user input by the AI
        self._dictionary_of_requirements_from_ai = {}

        # Variable to store the refined dataset after filtering and scoring the mobile phones based on user input
        self._refined_dataset = None

    def take_and_validate_user_input(self):
        """Method to take user input and validates it"""

        self._user_prompt = input(
            "Hey! Looking for a suitable mobile phone for your needs? We've got you covered. Type your requirements to get some AI based recommendations: "
        )

        instructions = None
        with open(
            os.path.join(
                self._ai_instructions_directory,
                "instructions_to_validate_user_input.txt",
            )
        ) as instructions_file:
            instructions = instructions_file.read()

        # Reading the instructions to extract information from the user input and passing it to the AIResponseGenerator class
        ai_response_generator = AIResponseGenerator(
            instructions=instructions, question=self._user_prompt
        )
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            ai_response_generator.get_answer()
        ai_response = str(captured_output.getvalue())
        print(ai_response)

        # If the user has entered a valid input, the AI will return a dictionary of requirements extracted from the user input.
        if "We have recieved your query" in ai_response:
            with open(
                os.path.join(
                    self._ai_instructions_directory,
                    "instructions_to_extract_information_from_user_input.txt",
                )
            ) as instructions_file:
                instructions = instructions_file.read()

            ai_response_generator = AIResponseGenerator(
                instructions=instructions, question=self._user_prompt
            )
            captured_output = io.StringIO()
            with contextlib.redirect_stdout(captured_output):
                ai_response_generator.get_answer()
            self._dictionary_of_requirements_from_ai = ast.literal_eval(
                captured_output.getvalue()
            )

    def clean_dataset(self):
        """Method that executes the class to clean up the DataSet"""

        # We clean up the dataset only if the refined dataset doesn't exist. If it exists, we don't clean up the dataset again.
        if not os.path.exists(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "refined_mobile_data",
                "RefinedMobileDataSet.csv",
            )
        ):
            data_cleaner = DataCleaner()
            data_cleaner.refine_existing_data()

    def rate_companies_models_and_processors(self):
        """Method that executes the classes to rate the unique companies, models and processors"""

        # Create the directory where the the refined CSV file will be stored
        directory_path = Path(
            os.path.join(os.path.dirname(__file__), "..", "ratings_files"),
            exist_ok=True,
        )
        directory_path.mkdir(exist_ok=True)

        # We rate the unique companies, models and processors only if the ratings JSON files don't exist. If they exist, we don't rate them again.
        if not os.path.exists(
            os.path.join(
                os.path.dirname(__file__), "..", "ratings_files", "company_ratings.json"
            )
        ):
            rate_unique_companies = RateUniqueCompanies()
            rate_unique_companies.generate_ratings()

        if not os.path.exists(
            os.path.join(
                os.path.dirname(__file__), "..", "ratings_files", "model_ratings.json"
            )
        ):
            rate_unique_models = RateUniqueModels()
            rate_unique_models.generate_ratings()

        if not os.path.exists(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "ratings_files",
                "processor_ratings.json",
            )
        ):
            rate_unique_processors = RateUniqueProcessors()
            rate_unique_processors.generate_ratings()

    def filter_mobiles_based_on_user_inputs(self):
        """Method that executes the class and method to filter the mobile phones based on user inputs"""
        filter_mobiles_based_on_user_inputs = FilterMobilesBasedOnUserInputs(
            self._dictionary_of_requirements_from_ai
        )
        filter_mobiles_based_on_user_inputs.filter_data_based_on_user_input()
        self._refined_dataset = (
            filter_mobiles_based_on_user_inputs.score_mobile_phones_based_on_user_input()
        )
        print(
            f"Found {len(self._refined_dataset)} mobile phones that match your requirements."
        )

    def display_recommended_mobile_phones_to_the_users(self):
        """Method to display recommended mobile phones to the users"""
        if len(self._refined_dataset) == 0:
            print(
                "Unfortunately there are no mobile phones that match your requirements. Please diversify your criteria or have a look at the top 5 best mobile phones that you can buy."
            )

        else:
            print(
                f"The best mobile phone for your requirements is: {self._refined_dataset.iloc[0]['Company Name']} {self._refined_dataset.iloc[0]['Model Name']}"
            )
            with open(
                os.path.join(
                    self._ai_instructions_directory,
                    "instructions_to_explain_choice.txt",
                )
            ) as instructions_file:
                instructions = instructions_file.read()

            # Reading the instructions to extract information from the user input and passing it to the AIResponseGenerator class
            ai_response_generator = AIResponseGenerator(
                instructions=instructions,
                question=f"Why is this mobile phone the best choice with the user requirements {self._user_prompt}? The mobile phone is: "
                + str(self._refined_dataset.iloc[0].to_dict()),
            )
            captured_output = io.StringIO()
            with contextlib.redirect_stdout(captured_output):
                ai_response_generator.get_answer()
            ai_response = str(captured_output.getvalue())
            print(ai_response)

            if len(self._refined_dataset) > 1:
                print(
                    f"Here are the other {len(self._refined_dataset)-1} mobile phone(s) that match your requirements:"
                )
                for company, model in zip(
                    self._refined_dataset["Company Name"],
                    self._refined_dataset["Model Name"],
                ):
                    print(f"{company} {model}")


if __name__ == "__main__":
    mobile_recommender = MobileRecommender()
    mobile_recommender.take_and_validate_user_input()
    mobile_recommender.clean_dataset()
    mobile_recommender.rate_companies_models_and_processors()
    mobile_recommender.filter_mobiles_based_on_user_inputs()
    mobile_recommender.display_recommended_mobile_phones_to_the_users()
