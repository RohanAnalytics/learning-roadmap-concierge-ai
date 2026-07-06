"""
app/agents/quiz_agent.py
------------------------

Quiz Agent

Uses QuizTool to generate quizzes for learners.
"""

from memory.context_manager import ContextManager
from app.agents.base_agent import BaseAgent
from tools.quiz_tool import QuizTool
from tools.profile_tool import ProfileTool
from tools.progress_storage_tool import ProgressStorageTool


class QuizAgent(BaseAgent):
    """Agent responsible for generating quizzes."""

    def __init__(self):

        self.tool = QuizTool()
        self.profile = ProfileTool()
        self.progress = ProgressStorageTool()
        self.context = ContextManager()

    @property
    def name(self) -> str:

        return "QuizAgent"

    @property
    def description(self) -> str:

        return "Generates quizzes."

    def process(self, user_input: str) -> str:

        profile = self.profile.get_profile("Rohan")
        
        if not profile:

            return (
                "Please create a learning roadmap first."
            )

        goal = profile.get("goal")

        progress = self.progress.get_progress("Rohan")

        course = progress.get(goal, {})

        remaining = course.get("remaining", [])

        if remaining:
            topic = remaining[0]
        else:
            topic = goal

        # -----------------------------
        # Update conversation context
        # -----------------------------

        self.context.set_goal(
            "default",
            goal,
        )

        self.context.set_current_topic(
            "default",
            topic,
        )

        self.context.set_last_agent(
            "default",
            self.name,
        )

        self.context.set_last_action(
            "default",
            "Generated Quiz",
        )

        quiz = self.tool.generate_quiz(topic)

        output = []

        output.append("# 📝 Knowledge Check\n")

        for index, question in enumerate(quiz, start=1):

            output.append(f"## Question {index}")

            output.append(question["question"])

            output.append("")

            for option in question["options"]:

                output.append(f"- {option}")

            output.append("")
            output.append(f"✅ Answer: {question['answer']}")
            output.append(f"📈 Difficulty: {question['difficulty']}")
            output.append(f"💡 Explanation: {question['explanation']}")
            output.append("")

        completed = course.get("completed", [])

        self.context.set_completed_topics(
            "default",
            completed,
        )

        self.context.set_remaining_topics(
            "default",
            remaining,
        )

        return "\n".join(output)