"""
tools/quiz_tool.py
------------------

AI Quiz Generation Tool

Generates personalized quizzes using Gemini.
Falls back to a local quiz database if Gemini
is unavailable.
"""

from __future__ import annotations

import json
import time
from typing import Dict, List

from google.genai import types

from app.model import get_client


class QuizTool:
    """Generate quizzes using Gemini with local fallback."""

    def __init__(self) -> None:

        self.client = get_client()

        self.database = {

            "python": [

                {
                    "question": "Which keyword defines a function?",
                    "options": ["func", "define", "def", "lambda"],
                    "answer": "def",
                    "difficulty": "Beginner",
                    "explanation": "Python uses the 'def' keyword."
                },

                {
                    "question": "Which data type is mutable?",
                    "options": ["tuple", "list", "str", "int"],
                    "answer": "list",
                    "difficulty": "Beginner",
                    "explanation": "Lists are mutable."
                }

            ],

            "numpy": [

                {
                    "question": "Which object stores NumPy data?",
                    "options": ["list", "ndarray", "tuple", "dict"],
                    "answer": "ndarray",
                    "difficulty": "Beginner",
                    "explanation": "NumPy stores data in ndarray."
                },

                {
                    "question": "Which function creates a NumPy array?",
                    "options": ["array()", "create()", "numpy()", "make()"],
                    "answer": "array()",
                    "difficulty": "Beginner",
                    "explanation": "numpy.array() creates arrays."
                }

            ],

            "pandas": [

                {
                    "question": "Which Pandas object stores tabular data?",
                    "options": ["Series", "DataFrame", "Array", "Matrix"],
                    "answer": "DataFrame",
                    "difficulty": "Beginner",
                    "explanation": "DataFrame stores rows and columns."
                },

                {
                    "question": "Which function reads a CSV file?",
                    "options": ["read_csv()", "load_csv()", "open_csv()", "csv()"],
                    "answer": "read_csv()",
                    "difficulty": "Beginner",
                    "explanation": "Pandas uses read_csv()."
                }

            ],

            "statistics": [

                {
                    "question": "Which measures the center of data?",
                    "options": ["Mean", "Range", "Variance", "Mode"],
                    "answer": "Mean",
                    "difficulty": "Beginner",
                    "explanation": "Mean is the average."
                },

                {
                    "question": "Standard deviation measures?",
                    "options": [
                        "Central tendency",
                        "Spread",
                        "Frequency",
                        "Probability"
                    ],
                    "answer": "Spread",
                    "difficulty": "Beginner",
                    "explanation": "Standard deviation measures dispersion."
                }

            ],

            "scikit-learn": [

                {
                    "question": "Which library provides train_test_split?",
                    "options": [
                        "NumPy",
                        "Scikit-Learn",
                        "TensorFlow",
                        "Pandas"
                    ],
                    "answer": "Scikit-Learn",
                    "difficulty": "Beginner",
                    "explanation": "train_test_split belongs to sklearn."
                },

                {
                    "question": "Which package contains machine learning models?",
                    "options": [
                        "sklearn",
                        "numpy",
                        "pandas",
                        "matplotlib"
                    ],
                    "answer": "sklearn",
                    "difficulty": "Beginner",
                    "explanation": "Machine learning models are in sklearn."
                }

            ],

            "regression": [

                {
                    "question": "Regression predicts?",
                    "options": [
                        "Continuous values",
                        "Categories",
                        "Images",
                        "Clusters"
                    ],
                    "answer": "Continuous values",
                    "difficulty": "Beginner",
                    "explanation": "Regression predicts numeric outputs."
                },

                {
                    "question": "Which algorithm is a regression algorithm?",
                    "options": [
                        "Linear Regression",
                        "K-Means",
                        "KNN",
                        "Naive Bayes"
                    ],
                    "answer": "Linear Regression",
                    "difficulty": "Beginner",
                    "explanation": "Linear Regression predicts continuous values."
                }

            ],

            "classification": [

                {
                    "question": "Classification predicts?",
                    "options": [
                        "Labels",
                        "Continuous values",
                        "Images",
                        "Clusters"
                    ],
                    "answer": "Labels",
                    "difficulty": "Beginner",
                    "explanation": "Classification predicts categories."
                },

                {
                    "question": "Which is a classification algorithm?",
                    "options": [
                        "Logistic Regression",
                        "Linear Regression",
                        "PCA",
                        "K-Means"
                    ],
                    "answer": "Logistic Regression",
                    "difficulty": "Beginner",
                    "explanation": "Logistic Regression is a classifier."
                }

            ],

            "clustering": [

                {
                    "question": "K-Means belongs to?",
                    "options": [
                        "Regression",
                        "Classification",
                        "Clustering",
                        "Deep Learning"
                    ],
                    "answer": "Clustering",
                    "difficulty": "Beginner",
                    "explanation": "K-Means groups similar data."
                },

                {
                    "question": "Clustering is?",
                    "options": [
                        "Supervised",
                        "Unsupervised",
                        "Reinforcement",
                        "Semi-supervised"
                    ],
                    "answer": "Unsupervised",
                    "difficulty": "Beginner",
                    "explanation": "Clustering is an unsupervised technique."
                }

            ],

            "model evaluation": [

                {
                    "question": "Accuracy measures?",
                    "options": [
                        "Correct predictions",
                        "Training speed",
                        "Model size",
                        "Dataset size"
                    ],
                    "answer": "Correct predictions",
                    "difficulty": "Beginner",
                    "explanation": "Accuracy measures prediction correctness."
                },

                {
                    "question": "Confusion Matrix is used for?",
                    "options": [
                        "Evaluation",
                        "Training",
                        "Cleaning Data",
                        "Deployment"
                    ],
                    "answer": "Evaluation",
                    "difficulty": "Beginner",
                    "explanation": "Confusion Matrix evaluates classifiers."
                }

            ],

            "deployment": [

                {
                    "question": "Which framework is commonly used to deploy ML APIs?",
                    "options": [
                        "FastAPI",
                "NumPy",
                        "Pandas",
                        "Matplotlib"
                    ],
                    "answer": "FastAPI",
                    "difficulty": "Beginner",
                    "explanation": "FastAPI is commonly used for ML APIs."
                },

                {
                    "question": "Deployment means?",
                    "options": [
                        "Making a model available to users",
                        "Training the model",
                        "Cleaning data",
                        "Collecting data"
                    ],
                    "answer": "Making a model available to users",
                    "difficulty": "Beginner",
                    "explanation": "Deployment makes models usable."
                }

            ],

            "power bi": [

                {
                    "question": "Which language is used to write measures?",
                    "options": ["SQL", "Python", "DAX", "R"],
                    "answer": "DAX",
                    "difficulty": "Beginner",
                    "explanation": "Measures use DAX."
                }

            ],

            "sql": [

                {
                    "question": "Which SQL statement retrieves data?",
                    "options": [
                        "UPDATE",
                        "DELETE",
                        "SELECT",
                        "INSERT"
                    ],
                    "answer": "SELECT",
                    "difficulty": "Beginner",
                    "explanation": "SELECT retrieves records."
                }

            ]

        }

    def generate_quiz(self, topic: str) -> List[Dict]:
        """
        Generate an AI quiz.

        Falls back to the local database if Gemini fails.
        """

        print(">>> AI QUIZ TOOL IS RUNNING <<<")

        prompt = f"""
You are an expert technical instructor.

Create a quiz about:

Topic: {topic}

Return ONLY valid JSON.

Example:

[
    {{
        "question":"...",
        "options":["A","B","C","D"],
        "answer":"A",
        "difficulty":"Beginner",
        "explanation":"..."
    }}
]

Rules:

- Generate exactly 5 questions.
- Four options per question.
- One correct answer.
- Mix conceptual and practical questions.
- Return ONLY JSON.
"""

        response = None

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.4,
                    ),
                )

                break

            except Exception as exc:

                print(
                    f"[QuizTool] Attempt {attempt + 1}/3 failed."
                )

                print(exc)

                if attempt < 2:
                    time.sleep(5)

        if response and response.text:

            print("\n========== QUIZ RESPONSE ==========\n")
            print(response.text)
            print("\n===================================\n")

            try:
                text = response.text.strip()

                if text.startswith("```json"):
                    text = text.replace("```json", "", 1)

                if text.startswith("```"):
                    text = text.replace("```", "", 1)

                if text.endswith("```"):
                    text = text[:-3]

                text = text.strip()

                quiz = json.loads(text)
                return quiz

            except json.JSONDecodeError:
                print("Invalid JSON returned by Gemini.")

        print("Using local quiz database.")

        topic = topic.lower().strip()

        for key in self.database:

            if key in topic:
                return self.database[key]

        return [

            {

                "question": "No quiz available.",

                "options": [],

                "answer": "",

                "difficulty": "N/A",

                "explanation": ""

            }

        ]