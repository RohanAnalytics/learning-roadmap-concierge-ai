"""
Progress Agent

Uses ProgressTool to calculate
learning progress.
"""

from app.agents.base_agent import BaseAgent
from tools.progress_storage_tool import ProgressStorageTool
from tools.profile_tool import ProfileTool
from memory.context_manager import ContextManager



class ProgressAgent(BaseAgent):

    def __init__(self):

        self.storage = ProgressStorageTool()
        self.profile = ProfileTool()
        self.context = ContextManager()

    @property
    def name(self):

        return "ProgressAgent"

    @property
    def description(self):

        return "Tracks learning progress."

    def process(self, user_input: str) -> str:

        profile = self.profile.get_profile("Rohan")

        goal = profile.get("goal", "")

        if not goal:
            return (
                "❌ No learning roadmap found.\n\n"
                "Create one first by typing:\n"
                "Create roadmap for Machine Learning"
            )

        text = user_input.lower()

        completion_phrases = [

            "complete ",

            "completed ",

            "mark ",

            "finished ",

            "i finished ",

        ]

        for phrase in completion_phrases:
            if text.startswith(phrase):
                parts = text.split(phrase, 1)
                if len(parts) < 2:
                    return "❌ Please specify which topic you completed."
                topic = parts[1]
                topic = topic.replace(" as completed", "")
                topic = topic.replace(" completed", "")
                topic = topic.strip().title()

                progress_data = self.storage.get_progress("Rohan")
                course = progress_data.get(goal, {})

                if not course.get("remaining"):

                    return (
                        "🎉 Your roadmap is already complete.\n"
                        "No more topics can be marked as completed."
                    )

                result = self.storage.mark_completed(
                    user="Rohan",
                    course=goal,
                    topic=topic,
                )

                progress_data = self.storage.get_progress("Rohan")
                course = progress_data.get(goal, {})

                self.context.initialize("default")
                self.context.set_completed_topics(
                    "default",
                    course.get("completed", [])
                )

                self.context.set_remaining_topics(
                    "default",
                    course.get("remaining", [])
                )

                remaining = course.get("remaining", [])

                self.context.set_current_topic(
                    "default",
                    remaining[0] if remaining else None
                )

                self.context.set_last_action(
                    "default",
                    f"Completed {topic}"
                )

                if result == "already_completed":
                    return f"✅ '{topic}' is already completed."

                if result == "topic_not_found":
                    return f"❌ '{topic}' doesn't exist in your roadmap."

                # -----------------------------
                # Update shared conversation context
                # -----------------------------


                if remaining:

                    next_topic = remaining[0]

                    return (
                        f"✅ Marked '{topic}' as completed for {goal}.\n\n"
                        f"🎯 Next Topic\n"
                        f"{next_topic}\n\n"
                        f"📝 Ready for a quick quiz?\n"
                        f"Type:\n"
                        f"Generate Quiz"
                    )

                return (
                    "🎉 Congratulations!\n\n"
                    "You have completed your roadmap."
                )
        progress = self.storage.get_progress("Rohan")
        course = progress.get(goal, {})

        completed = len(course.get("completed", []))
        remaining = len(course.get("remaining", []))
        total = completed + remaining
        percentage = 100 if total == 0 else round((completed / total) * 100)

        return (
            f"📈 Learning Progress\n\n"
            f"Goal: {goal}\n"
            f"Completed Topics: {completed}\n"
            f"Remaining Topics: {remaining}\n"
            f"Completion: {percentage}%"
        )