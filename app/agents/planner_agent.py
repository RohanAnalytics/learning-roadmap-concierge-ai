"""
Planner Agent

Uses RoadmapTool to generate structured learning plans.
Supports both AI-generated (Markdown) and fallback (dictionary) roadmaps.
"""

from __future__ import annotations

from app.agents.base_agent import BaseAgent
from skills.skill_analyzer import SkillAnalyzer
from tools.profile_tool import ProfileTool
from tools.roadmap_tool import RoadmapTool
from tools.progress_storage_tool import ProgressStorageTool
from memory.context_manager import ContextManager
from tools.analytics_tool import AnalyticsTool
from config.constants import DEFAULT_USER


class PlannerAgent(BaseAgent):
    """
    Planner Agent responsible for creating learning roadmaps.
    """

    def __init__(self) -> None:

        self.tool = RoadmapTool()
        self.context = ContextManager()
        self.analyzer = SkillAnalyzer()
        self.profile = ProfileTool()
        self.progress_storage = ProgressStorageTool()
        self.analytics = AnalyticsTool()

    @property
    def name(self) -> str:

        return "PlannerAgent"

    @property
    def description(self) -> str:

        return "Creates structured learning roadmaps."

    def process(
    self,
    user_input: str,
    weeks: int = 12,
) -> str:
        """
        Generate a roadmap from the user's request.
        """

        # -----------------------------------------
        # Extract requested skill
        # -----------------------------------------

        skill = user_input.strip()

        prefixes = [
            "Create a roadmap for ",
            "Create roadmap for ",
            "Roadmap for ",
            "Learn ",
            "Study ",
        ]

        for prefix in prefixes:
            if skill.lower().startswith(prefix.lower()):
                skill = skill[len(prefix):]
                break

        skill = skill.strip().title()
        if not skill:
            return "Please tell me what you'd like to learn."

        # -----------------------------------------
        # Analyze learner
        # -----------------------------------------

        analysis = self.analyzer.analyze(user_input)

        # -----------------------------------------
        # Save learner profile
        # -----------------------------------------

        self.profile.save_profile(
            DEFAULT_USER,
            {
                "goal": skill,
                "skills": analysis.get("known_skills", []),
                "missing_skills": analysis.get("missing_skills", []),
                "completed_topics": 0,
                "total_topics": 20,
                "current_level": analysis.get(
                    "current_level",
                    "Beginner",
                ),
                "recommended_level": analysis.get(
                    "recommended_level",
                    "Intermediate",
                ),
            },
        )
        

        # -----------------------------------------
        # Generate roadmap
        # -----------------------------------------

        roadmap = self.tool.generate(
            skill=skill,
            analysis=analysis,
            weeks=weeks,
        )

            
        if isinstance(roadmap, dict):

            progress = self.progress_storage.load_progress()

            if "users" not in progress:
                progress["users"] = {}

            progress.setdefault("users", {})
            progress["users"].setdefault(DEFAULT_USER, {})
            progress["users"][DEFAULT_USER][skill] = {
                "completed": [],
                "remaining": roadmap["topics"],
            }

            self.progress_storage.save_progress(progress)
            topics = roadmap.get("topics", [])

            self.context.initialize("default")

            self.context.set_goal(
                "default",
                skill,
            )

            self.context.set_current_topic(
                "default",
                topics[0] if topics else None,
            )

            self.context.set_completed_topics(
                "default",
                [],
            )

            self.context.set_remaining_topics(
                "default",
                topics,
            )

            self.context.set_last_agent(
                "default",
                self.name,
            )

            self.context.set_last_action(
                "default",
                "roadmap_created",
            )

        # -----------------------------------------
        # Gemini returned Markdown
        # -----------------------------------------

        if isinstance(roadmap, str):

            return roadmap

        # -----------------------------------------
        # Static fallback
        # -----------------------------------------

        output = []

        output.append(
            f"# Learning Roadmap for {roadmap['skill']}\n"
        )

        output.append(
        f"**Level:** {roadmap['level']}"
        )

        output.append(
        f"**Duration:** {roadmap['duration_weeks']} weeks\n"
        )

        for phase in roadmap["phases"]:

            output.append(f"## {phase['title']}")

            output.append(
                f"Duration: {phase['duration']}"
            )

            output.append("Topics:")

            for topic in phase["topics"]:

                output.append(f"- {topic}")

            output.append(
                f"Milestone: {phase['milestone']}\n"
            )

        try:
            analytics = self.analytics.analyze("Rohan")
        except Exception:
            analytics = None

        if analytics:

            output.append("\n")

            output.append("## 📊 Initial Learning Status")

            output.append(
                f"Completion: {analytics['completion']}%"
                )

            output.append(
                f"Current Phase: {analytics['phase']}"
            )

            output.append(
                f"Next Topic: {analytics['next_topic']}"
            )
        output.append("\nHappy Learning! 🚀")
        return "\n".join(output)