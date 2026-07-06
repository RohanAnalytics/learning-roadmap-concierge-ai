"""
tools/analytics_tool.py
-----------------------

Learning Analytics Tool

Calculates learning statistics from stored progress.
"""


from tools.progress_storage_tool import ProgressStorageTool
from tools.profile_tool import ProfileTool

from google.genai import types

import logging
logger = logging.getLogger(__name__)

from app.model import get_client, get_model_name


class AnalyticsTool:
    """Calculates learning analytics."""

    def __init__(self):

        self.progress = ProgressStorageTool()
        self.profile = ProfileTool()
        self.client = get_client()

    def analyze(self, user: str = "Rohan"):

        profile = self.profile.get_profile(user)

        if not profile:

            return None

        goal = profile.get("goal")

        if not goal:
            return None

        progress = self.progress.get_progress(user)

        course = progress.get(goal, {})

        completed = course.get("completed", [])

        remaining = course.get("remaining", [])

        total_topics = len(completed) + len(remaining)

        if total_topics == 0:

            completion = 0

        else:
            completion = round((len(completed) / total_topics) * 100)

        if completion < 34:

            phase = "Phase 1 - Foundations"

        elif completion < 67:

            phase = "Phase 2 - Intermediate"

        else:

            phase = "Phase 3 - Advanced"

        if remaining:

            next_topic = remaining[0]

            estimated_finish = (
                f"{len(remaining)} topic(s) remaining"
            )

        else:

            next_topic = "Roadmap Completed 🎉"

            estimated_finish = "Completed"
        
# ---------------------------------------------
# Generate AI Study Insights
# ---------------------------------------------

        prompt = f"""
        You are an expert learning mentor.

        Learning Goal:
        {goal}

        Completed Topics:
        {completed}

        Remaining Topics:
        {remaining}

        Completion:
        {completion}%

        Current Phase:
        {phase}

        Provide concise study insights.

        Include:

        - Progress summary
        - Strengths
        - Weaknesses
        - Recommended next focus
        - One motivation tip

        Limit to about 150 words.
        """

        try:

            response = self.client.models.generate_content(
                model=get_model_name(),
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                ),
            )

            insights = (
                response.text.strip()
                if getattr(response, "text", None)
                else "No AI insights available."
            )

        except Exception as exc:
            logger.warning("Gemini insights failed: %s", exc)

            insights = (
                f"You've completed {len(completed)} topic(s). "
                f"Your next focus should be '{next_topic}'. "
                "Maintain a consistent study schedule and practice regularly."
            )
# ------------------------------------
# Study recommendations
# ------------------------------------

        if completion < 34:

            recommended_pace = "3 topics/week"

            recommendation = (
                "Focus on building strong foundations before moving ahead."
                )

        elif completion < 67:

            recommended_pace = "2 topics/week"

            recommendation = (
                "Maintain consistency and practice each topic before continuing."
                )

        else:

            recommended_pace = "1-2 advanced topics/week"

            recommendation = (
                "Spend more time on projects and revision than new concepts."
                )
        return {

            "goal": goal,

            "completed": completed,

            "remaining": remaining,

            "completed_count": len(completed),

            "remaining_count": len(remaining),

            "completion": completion,

            "phase": phase,

            "next_topic": next_topic,

            "estimated_finish": estimated_finish,

            "insights": insights,

            "recommendation": recommendation,

            "recommended_pace": recommended_pace,
            }