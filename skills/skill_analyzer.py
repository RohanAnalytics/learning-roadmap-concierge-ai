"""
skill_analyzer.py

Uses Gemini to infer the user's current skill level,
known skills, missing skills, and recommended roadmap level.
"""

from __future__ import annotations

import json
import time

from google.genai import types

from app.model import get_client


class SkillAnalyzer:
    """
    AI-powered skill analyzer.
    """

    def __init__(self) -> None:
        self.client = get_client()

    def analyze(self, user_input: str) -> dict:
        """
        Analyze the learner's background using Gemini.

        Returns
        -------
        dict
            {
                "known_skills": [...],
                "missing_skills": [...],
                "current_level": "...",
                "recommended_level": "..."
            }

        If Gemini is unavailable, a fallback response is returned.
        """

        prompt = f"""
You are an expert technical career advisor.

Analyze the learner's background.

User Input:
{user_input}

Return ONLY valid JSON.

Example:

{{
  "known_skills": [
    "SQL",
    "Excel"
  ],
  "missing_skills": [
    "Python",
    "Statistics",
    "Machine Learning"
  ],
  "current_level": "Beginner",
  "recommended_level": "Intermediate"
}}

Rules:
- Return ONLY JSON.
- No markdown.
- No explanation.
"""

        response = None

        # Retry three times if Gemini free tier is busy
        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                    ),
                )

                break

            except Exception as exc:

                print(f"\nAttempt {attempt+1}/3 failed")
                print(exc)

                if attempt < 2:
                    print("Retrying in 5 seconds...\n")
                    time.sleep(5)

        # Gemini unavailable
        if response is None:

            print("\nGemini unavailable. Returning fallback.\n")

            return {
                "known_skills": [],
                "missing_skills": [],
                "current_level": "Unknown",
                "recommended_level": "Beginner",
            }

        # Empty response
        if not getattr(response, "text", None):

            print("\nGemini returned an empty response.\n")

            return {
                "known_skills": [],
                "missing_skills": [],
                "current_level": "Unknown",
                "recommended_level": "Beginner",
            }

        print("\n========== GEMINI RESPONSE ==========")
        print(response.text)
        print("=====================================\n")

        # Parse JSON
        try:

            return json.loads(response.text)

        except json.JSONDecodeError:

            print("Gemini returned invalid JSON.")
            print("Returning fallback.\n")

            return {
                "known_skills": [],
                "missing_skills": [],
                "current_level": "Unknown",
                "recommended_level": "Beginner",
            }

        except Exception as exc:

            print(exc)

            return {
                "known_skills": [],
                "missing_skills": [],
                "current_level": "Unknown",
                "recommended_level": "Beginner",
            }