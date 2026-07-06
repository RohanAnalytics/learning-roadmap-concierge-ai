"""
tools/resource_tool.py
----------------------

AI + Local Resource Recommendation Tool
"""

from __future__ import annotations

import time
import logging
logger = logging.getLogger(__name__)
from typing import Dict, List
from google.genai import types

from app.model import get_client
from app.model import get_model_name


class ResourceTool:
    """Provides AI and fallback learning resources."""

    def __init__(self) -> None:

        self.client = get_client()


        self.database = {

            "python": {

                "official_docs": [
                    "https://docs.python.org/3/"
                ],

                "youtube": [
                    "Programming with Mosh",
                    "Corey Schafer",
                    "freeCodeCamp"
                ],

                "courses": [
                    "Python for Everybody",
                    "100 Days of Code",
                    "CS50 Python"
                ],

                "books": [
                    "Automate the Boring Stuff",
                    "Python Crash Course"
                ],

                "practice": [
                    "LeetCode",
                    "HackerRank",
                    "Exercism"
                ],

            },

            "machine learning": {

                "official_docs": [
                    "https://scikit-learn.org/stable/",
                    "https://pytorch.org/docs/",
                    "https://www.tensorflow.org/learn"
                ],

                "youtube": [
                    "StatQuest",
                    "Krish Naik",
                    "Andrew Ng",
                    "freeCodeCamp"
                ],

                "courses": [
                    "Machine Learning Specialization",
                    "DeepLearning.AI",
                    "FastAI"
                ],

                "books": [
                    "Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow",
                    "Pattern Recognition and Machine Learning"
                ],

                "practice": [
                    "Kaggle",
                    "DrivenData",
                    "AIcrowd"
                ],

            },

            "power bi": {

                "official_docs": [
                    "https://learn.microsoft.com/power-bi/"
                ],

                "youtube": [
                    "Guy in a Cube",
                    "Pragmatic Works",
                    "Enterprise DNA"
                ],

                "courses": [
                    "Microsoft Learn",
                    "Maven Analytics",
                    "Udemy Power BI Bootcamp"
                ],

                "books": [
                    "The Definitive Guide to DAX",
                    "Power BI Cookbook"
                ],

                "practice": [
                    "Kaggle",
                    "DataDNA",
                    "Maven Challenges"
                ],

            },

            "sql": {

                "official_docs": [
                    "https://learn.microsoft.com/sql/"
                ],

                "youtube": [
                    "Alex The Analyst",
                    "freeCodeCamp"
                ],

                "courses": [
                    "SQLBolt",
                    "Mode SQL Tutorial"
                ],

                "books": [
                    "SQL Cookbook"
                ],

                "practice": [
                    "LeetCode",
                    "StrataScratch",
                    "HackerRank"
                ],

            },

        }

    def ai_resources(self, topic: str) -> str:
        """
        Generate AI-powered learning resources.
        Falls back to local recommendations when Gemini fails.
        """
        if not topic.strip():
            return "Please tell me which skill or topic you want learning resources for."

        prompt = f"""
You are an expert technical mentor.

Recommend the BEST learning resources for:

Learning Goal:
{topic}

Return Markdown.

Include:

# Learning Resources

## Official Documentation

## Best Free Courses

## Best Paid Courses

## YouTube Channels

## Books

## Practice Websites

## GitHub Repositories

## Communities

## Certifications

## Mini Projects

Explain each recommendation in 1-2 concise lines.
"""

        response = None

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model=get_model_name(),
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.4,
                    ),
                )

                break

            except Exception as exc:

                if attempt < 2:
                    time.sleep(2)
                    logger.warning(
                        "Gemini resource generation failed (Attempt %d/3): %s",
                        attempt + 1,
                        exc,
                    )

        if response and getattr(response, "text", None):
            return response.text

        logger.info("Using local fallback resource database.")

        fallback = self.get_resources(topic)

        output = []

        output.append("# 📚 Learning Resources\n")

        for category, items in fallback.items():

            output.append(f"## {category.replace('_', ' ').title()}")

            for item in items:
                output.append(f"- {item}")

            output.append("")

        return "\n".join(output)

    def get_resources(self, topic: str) -> Dict[str, List[str]]:
        """
        Return curated learning resources.
        """

        topic = topic.lower().strip()

        for key in sorted(self.database.keys()):

            if key in topic:

                return self.database[key]

        return {

            "official_docs": [
                "Official Documentation"
            ],

            "youtube": [
                "freeCodeCamp"
            ],

            "courses": [
                "Coursera"
            ],

            "books": [
                "Search Amazon or O'Reilly for highly rated books."
            ],

            "practice": [
                "Kaggle"
            ],

        }