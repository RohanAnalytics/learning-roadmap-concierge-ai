"""
app/agents/analytics_agent.py
-----------------------------

Analytics Agent

Displays learning analytics and study recommendations.
"""

from app.agents.base_agent import BaseAgent
from tools.analytics_tool import AnalyticsTool


class AnalyticsAgent(BaseAgent):

    def __init__(self):

        self.tool = AnalyticsTool()

    @property
    def name(self):

        return "AnalyticsAgent"

    @property
    def description(self):

        return "Shows learning analytics."

    def process(self, user_input: str):

        analytics = self.tool.analyze("Rohan")

        if analytics is None:

            return (
                "❌ No learning roadmap found.\n\n"
                "Create one first by typing:\n"
                "Create roadmap for Machine Learning"
            )

        output = []

        output.append("# 📊 Learning Analytics\n")

        output.append(f"Learning Goal: {analytics['goal']}\n")

        output.append(
            f"Completed Topics: {analytics['completed_count']}"
        )

        output.append(
            f"Remaining Topics: {analytics['remaining_count']}"
        )

        output.append(
            f"Completion: {analytics['completion']}%"
        )

        output.append(
            f"Current Phase: {analytics['phase']}"
        )

        output.append(
            f"Next Topic: {analytics['next_topic']}"
        )

        output.append(
            f"Estimated Finish: {analytics['estimated_finish']}"
        )
        output.append(
            f"Recommended Pace: {analytics['recommended_pace']}"
            )
        output.append(
            f"\n💡 Recommendation"
            )
        output.append(
            analytics["recommendation"]
)

        output.append("\n✅ Completed Topics")

        if analytics["completed"]:

            for topic in analytics["completed"]:

                output.append(f"- {topic}")

        else:

            output.append("- None")

        output.append("\n⏳ Remaining Topics")

        if analytics["remaining"]:

            for topic in analytics["remaining"]:

                output.append(f"- {topic}")

        else:

            output.append("🎉 Roadmap Completed!")

            output.append("\n💡 AI Study Insights\n")

            output.append(analytics["insights"])

            output.append("\n🚀 Smart Recommendations\n")

            output.append(analytics["recommendation"])

        return "\n".join(output)