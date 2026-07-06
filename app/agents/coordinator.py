"""
app/agents/coordinator.py
--------------------------

Coordinator Agent for the Learning Roadmap Concierge AI.

This module serves as the orchestration layer of the application.

Responsibilities
----------------
• Receive every user request.
• Determine which specialist agent should process it.
• Route the request.
• Return the final response.
• Maintain session information.
• Provide centralized logging.

The coordinator is intentionally designed so it can later be
converted into a Google ADK Root Agent with minimal changes.
"""

from __future__ import annotations

from config.constants import DEFAULT_USER

import logging
import uuid
from typing import Any
from typing import Dict
from typing import Set
from typing import Type


from app.agent import LearningRoadmapAgent
from app.agents.base_agent import BaseAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.profile_agent import ProfileAgent
from app.agents.resource_agent import ResourceAgent
from app.agents.quiz_agent import QuizAgent
from app.agents.progress_agent import ProgressAgent
from app.agents.analytics_agent import AnalyticsAgent
from memory import MemoryManager
from memory.context_manager import ContextManager
from tools.analytics_tool import AnalyticsTool





# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s",

)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Default Learning Roadmap Adapter
# ---------------------------------------------------------

class DefaultRoadmapAgent(BaseAgent):
    """
    Adapter around the original LearningRoadmapAgent.

    The original agent was developed before the multi-agent
    architecture existed.

    This adapter allows the coordinator to treat it like any
    other BaseAgent without changing its implementation.
    """

    def __init__(self):

        self._agent = LearningRoadmapAgent()

    @property
    def name(self) -> str:

        return "LearningRoadmapAgent"

    @property
    def description(self) -> str:

        return (
            "Default Gemini-powered roadmap generation agent."
        )

    def process(self, user_input: str) -> str:

        return self._agent.chat(user_input)


# ---------------------------------------------------------
# Routing Table
# ---------------------------------------------------------

ROUTES = [

    {

        "agent": ProfileAgent,

        "keywords": {

            "profile",

            "experience",

            "background",

            "my level",

            "who am i",

            "my skills",

            "my profile",

            "extract my info",

        },

    },

    {

        "agent": PlannerAgent,

        "keywords": {

            "roadmap",

            "plan",

            "learning path",

            "study plan",

            "career plan",

            "schedule",

            "timeline",

            "learning roadmap",

        },

    },

    {

        "agent": ResourceAgent,

        "keywords": {

            "resources",

            "courses",

            "books",

            "youtube",

            "tutorials",

            "documentation",

            "where can i learn",

            "recommend",

            "materials",

        },

    },
    
    {
        "agent": QuizAgent,
        "keywords": {
            "quiz",
            "test me",
            "practice test",
            "questions",
            "mcq",
            "assessment",
            "knowledge check",
        },
    },

    {
        "agent": ProgressAgent,
        "keywords": {
            "progress",
            "my progress",
            "track progress",
            "learning progress",
            "completion",
            "status",
            "how much have i completed",
            "complete ",
            "completed ",
            "finished ",
            "i finished ",
            "mark ",
        },
    },

    {
        "agent": AnalyticsAgent,
        "keywords": {
            "analytics",
            "analysis",
            "insights",
            "report",
            "statistics",
            "study stats",
            "performance",
            "show analytics",
            "learning analytics",
            "how am i doing",
            "am i on track",
        },
    },
]

# ---------------------------------------------------------
# Coordinator Agent
# ---------------------------------------------------------

class CoordinatorAgent(BaseAgent):
    """
    Central orchestrator for the Learning Roadmap Concierge AI.

    Every request from the CLI or future web interface enters
    through this class.

    Responsibilities
    ----------------
    • Maintain session state
    • Select the correct specialist
    • Route requests
    • Log execution
    • Return the final response
    """

    def __init__(
        self,
        session_id: str | None = None,
        use_adk: bool = False,
    ) -> None:

        self.use_adk = use_adk
    
        self.session_id = session_id or str(uuid.uuid4())

        self._default_agent = DefaultRoadmapAgent()

        self._specialists: Dict[
            Type[BaseAgent],
            BaseAgent,
        ] = {}

        self._memory: MemoryManager = MemoryManager()
        self._context = ContextManager()
        self._context.initialize(self.session_id)
        self.analytics = AnalyticsTool()


        self._turn_counter: int = 0

        logger.info(
            "Coordinator initialized | Session=%s",
            self.session_id,
        )

    # -------------------------------------------------

    @property
    def name(self) -> str:

        return "CoordinatorAgent"

    @property
    def description(self) -> str:

        return (
            "Routes user requests to the correct "
            "specialized AI agent."
        )

    # -------------------------------------------------

    def process(
        self,
        user_input: str,
    ) -> str:
        """
        Process a user request.

        Parameters
        ----------
        user_input : str

            Raw user message.

        Returns
        -------
        str

            Final response from the selected agent.
        """

        self._validate(user_input)

        self._turn_counter += 1
        turn_key = f"turn_{self._turn_counter}"

        logger.info(
            "Session=%s | Turn=%d | User=%s",
            self.session_id,
            self._turn_counter,
            user_input,
        )

        # Persist the incoming user message.
        self._memory.save(
            self.session_id,
            f"{turn_key}_input",
            user_input,
        )

        selected_agent = self._select_agent(user_input)
        self._context.set_last_agent(
            self.session_id,
            selected_agent.name,
        )

        self._context.set_last_action(
            self.session_id,
            user_input,
        )

        # Persist which agent was selected for this turn.
        self._memory.save(
            self.session_id,
            f"{turn_key}_agent",
            selected_agent.name,
        )

        logger.info(
            "Routing request to %s",
            selected_agent.name,
        )

        response = selected_agent.process(user_input)

        # ---------------------------------------------
        # Coordinator enhancement for Progress requests
        # ---------------------------------------------

        if selected_agent.name == "ProgressAgent":

            analytics = self.analytics.analyze(DEFAULT_USER)

            if analytics:

                response += "\n\n"

                response += "📊 Learning Summary\n\n"

                response += (
                    f"Current Phase: {analytics['phase']}\n"
                )

                response += (
                    f"Completion: {analytics['completion']}%\n"
                )

                response += (
                    f"Recommended Pace: {analytics['recommended_pace']}\n"
                )
                
        # Persist the AI response.
        self._memory.save(
            self.session_id,
            f"{turn_key}_response",
            response,
        )

        # Keep a running list of every user message for quick retrieval.
        history: list[str] = self._memory.load(
            self.session_id, "input_history"
        ) or []
        history.append(user_input)
        self._memory.save(self.session_id, "input_history", history)

        logger.info(
            "Response generated successfully | Turn=%d",
            self._turn_counter,
        )

        return response

    # -------------------------------------------------

    def _select_agent(
        self,
        user_input: str,
    ) -> BaseAgent:
        """
        Select the most appropriate agent.

        Current implementation uses keyword routing.

        Later this function will be replaced with
        Gemini Intent Detection via Google ADK.
        """

        text = user_input.lower()

        for route in ROUTES:

            if self._contains_keyword(
                text,
                route["keywords"],
            ):

                return self._get_agent(
                    route["agent"]
                )

        logger.info(
            "No specialist matched."
        )

        return self._default_agent

        # -------------------------------------------------

    def _get_agent(
        self,
        agent_class: Type[BaseAgent],
    ) -> BaseAgent:
        """
        Return a cached specialist agent.

        Agents are lazily initialized. The first time an
        agent is needed, it is created and stored.
        Subsequent requests reuse the same instance.
        """

        if agent_class not in self._specialists:

            logger.info(
                "Initializing specialist: %s",
                agent_class.__name__,
            )

            self._specialists[agent_class] = agent_class()

        return self._specialists[agent_class]

    # -------------------------------------------------

    @staticmethod
    def _contains_keyword(
        text: str,
        keywords: Set[str],
    ) -> bool:
        """
        Return True if any routing keyword
        exists in the user input.
        """

        text = text.lower().strip()

        return any(
            keyword.lower() in text
            for keyword in keywords
        )

    # -------------------------------------------------

    @staticmethod
    def _validate(
        text: str,
    ) -> None:
        """
        Validate user input before routing.
        """

        if text is None:

            raise ValueError(
                "User input cannot be empty."
            )

        if not text.strip():

            raise ValueError(
                "User input cannot be blank."
            )

    # -------------------------------------------------

    def get_memory(self) -> dict[str, Any]:
        """
        Return a snapshot of the full session memory.

        The returned dictionary contains every key saved during
        this session: per-turn inputs, agent names, responses,
        and the consolidated ``input_history`` list.

        Returns
        -------
        dict[str, Any]
            Shallow copy of the current session's memory store.
        """

        return self._memory.load_all(self.session_id)

    # -------------------------------------------------

    def clear_memory(self) -> None:
        """
        Erase all memory for the current session.

        Resets the turn counter so a cleared session starts
        fresh without generating duplicate turn keys.

        Useful when the user explicitly asks to start over or
        when an automated test needs a clean slate.
        """

        self._memory.clear(self.session_id)
        self._context.clear(self.session_id)
        self._turn_counter = 0

        logger.info(
            "Memory cleared | Session=%s",
            self.session_id,
        )
    # -------------------------------------------------

    def reset_session(self) -> None:
        """
        Clear all cached specialist agents and session memory.

        This is useful when starting a completely
        new conversation or resetting application state.
        """

        self._specialists.clear()

        self.clear_memory()

        self._context.initialize(self.session_id)

        logger.info(
            "Session reset | Session=%s",
            self.session_id,
        )

    # -------------------------------------------------

    def get_session_id(self) -> str:
        """
        Return the active session ID.
        """

        return self.session_id

    # -------------------------------------------------

    def get_loaded_agents(self) -> list[str]: 
        """
        Return the names of all currently
        initialized specialist agents.

        Helpful for debugging and future
        monitoring dashboards.
        """
        return [
        agent.name
        for agent in self._specialists.values()
        ]

    # -------------------------------------------------

    def get_context(self) -> dict:
        return self._context.get(self.session_id)

# =========================================================
# End of File
# =========================================================