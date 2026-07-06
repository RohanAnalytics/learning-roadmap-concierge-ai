"""
agent.py
---------

Core AI Agent for the Learning Roadmap Concierge.

This module connects the Gemini model, system prompt,
and reusable client into a single interface that
future Google ADK agents can build upon.
"""

from google.genai import types

from app.model import (
    get_client,
    get_model_name,
)

from app.prompts import (
    SYSTEM_PROMPT,
)


class LearningRoadmapAgent:
    """
    AI Learning Concierge Agent.

    Responsible for generating personalized learning
    roadmaps using Gemini.
    """

    def __init__(self):

        self.client = get_client()

        self.model = get_model_name()

    def chat(self, user_message: str) -> str:
        """
        Generate a response from Gemini.

        Parameters
        ----------
        user_message : str

            User input.

        Returns
        -------
        str

            AI response.
        """

        if not user_message.strip():

            raise ValueError(
                "User message cannot be empty."
            )

        try:

            response = self.client.models.generate_content(

                model=self.model,

                contents=user_message,

                config=types.GenerateContentConfig(

                    system_instruction=SYSTEM_PROMPT,

                    temperature=0.7,

                ),

            )

            if response.text:

                return response.text

            return (
                "I couldn't generate a response."
            )

        except Exception as error:

            return (
                f"An error occurred while contacting "
                f"the AI model:\n\n{error}"
            )