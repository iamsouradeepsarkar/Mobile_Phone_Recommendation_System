"""
Main module
"""

import contextlib
import io
import os
import ast

from data_cleaner import DataCleaner
from ai_response_generator import AIResponseGenerator
from filter_mobiles_based_on_user_inputs import FilterMobilesBasedOnUserInputs

class MobileRecommender:
    """Class to recommend mobile phones based on user inputs"""

    def __init__(self):
        """Constructor of the MobileRecommender class"""
        self._user_prompt = None
        self._ai_instructions_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instructions")
        self._dictionary_of_requirements_from_ai = {}

    def take_and_validate_user_input(self):
        """Method to take user input and validates it"""
        self._user_prompt = input("Hey! Looking for a suitable mobile phone for your needs? We've got you covered. Type your requirements to get some AI based recommendations: ")

        instructions = None
        with open(os.path.join(self._ai_instructions_directory, "instructions_to_validate_user_input.txt")) as instructions_file:
            instructions = instructions_file.read()

        ai_response_generator = AIResponseGenerator(instructions=instructions, question=self._user_prompt)
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            ai_response_generator.get_answer()
        ai_response = str(captured_output.getvalue())
        print(ai_response)
        if "We have recieved your query" in ai_response:
            with open(os.path.join(self._ai_instructions_directory, "instructions_to_extract_information_from_user_input.txt")) as instructions_file:
                    instructions = instructions_file.read()
            
            ai_response_generator = AIResponseGenerator(instructions=instructions, question=self._user_prompt)
            captured_output = io.StringIO()
            with contextlib.redirect_stdout(captured_output):
                ai_response_generator.get_answer()
            self._dictionary_of_requirements_from_ai = ast.literal_eval(captured_output.getvalue())
            print(self._dictionary_of_requirements_from_ai)

    def clean_dataset(self):
        """Method that executes the class to clean up the DataSet"""
        data_cleaner = DataCleaner()
        data_cleaner.refine_existing_data()

    def filter_mobiles_based_on_user_inputs(self):
        """Method that executes the class and method to filter the mobile phones based on user inputs"""
        filter_mobiles_based_on_user_inputs = FilterMobilesBasedOnUserInputs(self._dictionary_of_requirements_from_ai)
        filter_mobiles_based_on_user_inputs.recommender()
        
        
        
if __name__ == "__main__":
    mobile_recommender = MobileRecommender()
    mobile_recommender.take_and_validate_user_input()
    mobile_recommender.clean_dataset()
    mobile_recommender.filter_mobiles_based_on_user_inputs()