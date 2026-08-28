"""
__main__.py module for the Mobile Phone Recommendation System package.
This module serves as the entry point for the Mobile Phone Recommendation System package. It imports the MobileRecommender class from the main module and executes its methods to take user input, clean the dataset, rate unique companies, models, and processors, filter mobile phones based on user inputs, and display recommended mobile phones to the users.
"""

from .main import MobileRecommender

mobile_recommender = MobileRecommender()
mobile_recommender.take_and_validate_user_input()
mobile_recommender.clean_dataset()
mobile_recommender.rate_companies_models_and_processors()
if mobile_recommender._dictionary_of_requirements_from_ai:
    mobile_recommender.filter_mobiles_based_on_user_inputs()
    mobile_recommender.display_recommended_mobile_phones_to_the_users()
