"""
tools/progress_tool.py
----------------------

AI Progress Tracking Tool

Uses Gemini to generate personalized progress
feedback while keeping deterministic progress
calculations as a fallback.
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta

from google.genai import types

from app.model import get_client


class ProgressTool:
    """Tracks learner progress."""

    def __init__(self) -> None:

        self.client = get_client()

    def calculate_progress(
        self,
        total_topics: int,
        completed_topics: int,
    ) -> dict:
        """
        Calculate learner progress.

        Uses Gemini for personalized feedback.
        Falls back to deterministic calculations.
        """

        print(">>> AI PROGRESS TOOL IS RUNNING <<<")

        prompt = f"""
You are an expert learning mentor.

A learner has completed:

Completed Topics: {completed_topics}

Total Topics: {total_topics}

Return ONLY valid JSON.

Example:

{{
    "completed_topics": 8,
    "remaining_topics": 12,
    "completion_percentage": 40,
    "current_phase": "Intermediate",
    "estimated_finish": "15 August 2026",
    "next_milestone": "Finish Feature Engineering"
}}

Return ONLY JSON.
"""

        response = None

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                    ),
                )

                break

            except Exception as exc:

                print(
                    f"[ProgressTool] Attempt {attempt + 1}/3 failed."
                )

                print(exc)

                if attempt < 2:
                    time.sleep(5)

        if response and response.text:

            print("\n========== PROGRESS RESPONSE ==========\n")
            print(response.text)
            print("\n=======================================\n")

            try:

                import json

                return json.loads(response.text)

            except Exception:

                print("Gemini returned invalid JSON.")
                print("Using local calculation.")

        # ---------- Local fallback ----------

        if total_topics <= 0:
            total_topics = 1

        percentage = round(
            (completed_topics / total_topics) * 100,
            2,
        )

        remaining = total_topics - completed_topics

        days_remaining = remaining * 2

        estimated_finish = (
            datetime.today() +
            timedelta(days=days_remaining)
        ).strftime("%d %B %Y")

        if percentage < 30:

            phase = "Foundation"

        elif percentage < 70:

            phase = "Intermediate"

        else:

            phase = "Advanced"

        return {

            "completed_topics": completed_topics,

            "remaining_topics": remaining,

            "completion_percentage": percentage,

            "current_phase": phase,

            "estimated_finish": estimated_finish,

            "next_milestone": "Complete the next learning module."

        }