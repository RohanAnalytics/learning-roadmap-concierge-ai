"""
app/agents/__init__.py
----------------------

Public surface of the multi-agent package.

Importing from this package gives access to every concrete agent and
the abstract base without having to know the internal module layout.
"""

from app.agents.base_agent import BaseAgent
from app.agents.coordinator import CoordinatorAgent
from app.agents.profile_agent import ProfileAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.resource_agent import ResourceAgent
from app.agents.quiz_agent import QuizAgent
from app.agents.progress_agent import ProgressAgent
from app.agents.analytics_agent import AnalyticsAgent

__all__ = [
    "BaseAgent",
    "CoordinatorAgent",
    "ProfileAgent",
    "PlannerAgent",
    "ResourceAgent",
    "QuizAgent",
    "ProgressAgent",
    "AnalyticsAgent",
]
