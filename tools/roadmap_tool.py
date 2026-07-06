"""
roadmap_tool.py

Generates structured learning roadmaps for the Learning Roadmap Concierge AI.
Uses Gemini to generate dynamic roadmaps with a static fallback if the API
is unavailable.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Union


from app.model import get_client
from app.model import get_model_name
from app.prompts import SYSTEM_PROMPT


@dataclass
class RoadmapPhase:
    """
    Represents one phase of a learning roadmap.
    """

    title: str
    duration: str
    topics: List[str]
    milestone: str


class RoadmapTool:
    """
    Generates structured learning roadmaps.

    Workflow:
        1. Try Gemini.
        2. If Gemini fails, return the built-in roadmap.
    """

    def __init__(self) -> None:
        self.client = get_client()
        self.model = get_model_name()

        self.roadmap_catalog = {

        "Machine Learning": [

            "Python Basics",
            "NumPy",
            "Pandas",
            "Statistics",
            "Scikit-Learn",
            "Regression",
            "Classification",
            "Clustering",
            "Model Evaluation",
            "Deployment",

        ],

        "Data Analytics": [

            "Excel",
            "SQL",
            "Python",
            "Pandas",
            "Data Cleaning",
            "Data Visualization",
            "Power BI",
            "Statistics",
            "Dashboard Design",
            "Business Insights",

        ],

        "Deep Learning": [

            "Python Basics",
            "NumPy",
            "Linear Algebra",
            "Neural Networks",
            "TensorFlow",
            "PyTorch",
            "CNN",
            "RNN",
            "Transformers",
            "Deployment",

        ],

    }

    def generate(
        self,
        skill: str,
        analysis: dict | None = None,
        weeks: int = 12,
    ) -> Union[str, dict]:
        """
        Generate a learning roadmap.

        Parameters
        ----------
        skill : str
            Skill to learn.

        level : str
            Current experience level.

        weeks : int
            Target duration.

        Returns
        -------
        str | dict

        Returns Markdown text when Gemini succeeds.
        Returns a structured dictionary if Gemini is unavailable.
        """

        known = ", ".join(
            analysis.get("known_skills", [])
        ) if analysis else "Unknown"

        missing = ", ".join(
            analysis.get("missing_skills", [])
        ) if analysis else "Unknown"

        current = (
            analysis.get("current_level", "Beginner")
            if analysis else "Beginner"
        )

        recommended = (
            analysis.get("recommended_level", "Intermediate")
            if analysis else "Intermediate"
        )
        roadmap_topics = self.roadmap_catalog.get(skill)

        prompt = f"""
        {SYSTEM_PROMPT}
You are an expert learning mentor.

Create a highly personalized learning roadmap.

Skill Goal:
{skill}

Current Level:
{current}

Recommended Level:
{recommended}

Known Skills:
{known}

Missing Skills:
{missing}

Duration:
{weeks} weeks

Return markdown.

Include:

# Learning Goal

## Current Situation

## Personalized Roadmap

### Phase 1

### Phase 2

### Phase 3

## Final Project

## Interview Preparation

## Recommended Next Steps
"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            if response and response.text:
                return response.text

        except Exception as e:

            print(f"Gemini failed: {e}")

        # --------------------------------------------------------
        # Static fallback roadmap
        # --------------------------------------------------------

        if roadmap_topics is None:

            roadmap_topics = [

                f"Introduction to {skill}",
                "Core Concepts",
                "Basic Practice",
                "Hands-on Exercises",
                "Mini Projects",
                "Problem Solving",
                "Real-world Project",
                "Best Practices",
                "Interview Preparation",

            ]

        phase_size = math.ceil(len(roadmap_topics) / 3)

        phases = [

            RoadmapPhase(

                title="Phase 1 - Foundations",

                duration=f"Week 1 - {max(1, weeks//3)}",

                topics=roadmap_topics[:phase_size],

                milestone="Complete Foundation Topics.",

            ),

            RoadmapPhase(

                title="Phase 2 - Intermediate",

                duration=f"Week {weeks//3 + 1} - {(weeks//3) * 2}",

                topics=roadmap_topics[phase_size:2*phase_size],

                milestone="Complete Intermediate Topics.",

            ),

            RoadmapPhase(

                title="Phase 3 - Advanced",

                duration=f"Week {(weeks//3) * 2 + 1} - {weeks}",

                topics=roadmap_topics[2*phase_size:],

                milestone="Complete Advanced Topics.",

            ),

        ]
        
        return {

            "skill": skill,

            "level": current,

            "duration_weeks": weeks,

            "topics": roadmap_topics,

            "phases": [

                {
                    "title": phase.title,
                    "duration": phase.duration,
                    "topics": phase.topics,
                    "milestone": phase.milestone,
                }

                for phase in phases

            ],

        }