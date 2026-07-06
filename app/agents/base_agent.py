"""
app/agents/base_agent.py
------------------------

Abstract base class that every specialized agent must inherit.

Defining a shared contract here keeps the coordinator decoupled from
concrete implementations and makes the system trivially extensible:
adding a new specialist only requires subclassing BaseAgent and
registering it with the CoordinatorAgent.
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Shared interface for all Learning Roadmap Concierge agents.

    Every agent in the system inherits from this class, guaranteeing
    that the :class:`~app.agents.coordinator.CoordinatorAgent` can
    always call :meth:`process` without knowing the concrete type.

    Subclasses must override :attr:`name`, :attr:`description`, and
    :meth:`process`.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable identifier for this agent.

        Used by the coordinator when logging which specialist handled
        a request and in future ADK agent registries.

        Returns:
            str: A short, unique name such as ``"ProfileAgent"``.
        """

    @property
    @abstractmethod
    def description(self) -> str:
        """One-sentence summary of what this agent does.

        Used by the coordinator to select the right specialist and
        to surface agent metadata in admin/debug views.

        Returns:
            str: Plain-English description of the agent's purpose.
        """

    @abstractmethod
    def process(self, user_input: str) -> str:
        """Handle a single user turn and return a response string.

        This is the single entry point the coordinator calls.  Each
        specialist implements its own strategy here — from a pure
        regex parser to a full Gemini round-trip.

        Args:
            user_input: Raw text submitted by the user in this turn.

        Returns:
            str: The agent's response, ready to be printed to the user.

        Raises:
            ValueError: If ``user_input`` is blank.
        """

