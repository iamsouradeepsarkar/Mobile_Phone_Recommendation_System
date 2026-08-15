"""
Module to send instructions to the AI models and generate responses.
"""
from ollama import Client

class AIResponseGenerator:
    """AIResponseGenerator class to take the query and provide relevant responses to the users"""

    def __init__(self, instructions, question):
        """Constructor of the AIResponseGenerator class"""

        self.client = Client()
        self._instructions = instructions
        self._question = question
        self._response = None

    def get_answer(self):
        """Method to send instructions and question to the AI model."""

        self.messages = [
            # 1. System role: The instruction to the AI model.
            {
                "role": "system",
                "content": self._instructions,
            },
            # 2. User role: The human's first question to the model.
            {
                "role": "user",
                "content": self._question,
            },
            ]

        # Using gpt-oss as the model. Other models can be found here: https://ollama.com/search
        for part in self.client.chat('gpt-oss:120b-cloud', messages=self.messages, stream=True):
            self._response = part.message.content
            print(self._response, end="",)
