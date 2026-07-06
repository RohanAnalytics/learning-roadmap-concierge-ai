"""
app/agents/resource_agent.py
----------------------------

Resource Agent

Provides personalized learning resources.
"""

from app.agents.base_agent import BaseAgent
from tools.resource_tool import ResourceTool
from tools.profile_tool import ProfileTool
from tools.progress_storage_tool import ProgressStorageTool
from config.constants import DEFAULT_USER

class ResourceAgent(BaseAgent):

    def __init__(self):
        self.tool = ResourceTool()
        self.profile = ProfileTool()
        self.progress = ProgressStorageTool()

    @property
    def name(self):

        return "ResourceAgent"

    @property
    def description(self):

        return "Provides personalized learning resources."

    def process(self, user_input: str):
        profile = self.profile.get_profile(DEFAULT_USER)

        if not profile:

            return "Please create a learning roadmap first."

        goal = profile.get("goal","")

        progress = self.progress.get_progress(DEFAULT_USER)

        course = progress.get(goal, {})

        remaining = course.get("remaining", [])

        if remaining:

            topic = remaining[0]

        else:
            topic = goal

        return self.tool.ai_resources(topic)