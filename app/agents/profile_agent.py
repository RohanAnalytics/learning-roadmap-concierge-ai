"""
app/agents/profile_agent.py
----------------------------

Stateless NLP-lite agent that extracts structured learner metadata
from free-form text — no AI call required.

The extracted profile is a plain dictionary that downstream agents
(PlannerAgent, ResourceAgent) can consume to personalise their
output without re-asking the user for the same information.
"""

import re
from typing import Any

from app.agents.base_agent import BaseAgent


# ---------------------------------------------------------------------------
# Pattern library
# ---------------------------------------------------------------------------

_GOAL_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\blearn(?:ing)?\s+(.+?)(?:\s+in\s+|\s+within\s+|\s+over\s+|$)", re.I),
    re.compile(r"\bwant\s+to\s+(?:learn|master|study|understand)\s+(.+?)(?:\s+in\s+|\.|$)", re.I),
    re.compile(r"\bgoal\s+is\s+to\s+(.+?)(?:\.|$)", re.I),
    re.compile(r"\bbecome\s+(?:a\s+)?(.+?)(?:\s+in\s+|\.|$)", re.I),
]

_TIMELINE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\bin\s+(\d+\s+(?:day|week|month|year)s?)\b", re.I),
    re.compile(r"\bwithin\s+(\d+\s+(?:day|week|month|year)s?)\b", re.I),
    re.compile(r"\bover\s+(?:the\s+next\s+)?(\d+\s+(?:day|week|month|year)s?)\b", re.I),
    re.compile(r"\b(\d+)[- ](?:day|week|month|year)\s+(?:plan|roadmap|course|timeline)\b", re.I),
]

_HOURS_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b(\d+)\s+hours?\s+(?:a|per)\s+(?:day|week)\b", re.I),
    re.compile(r"\bspend\s+(\d+)\s+hours?\b", re.I),
    re.compile(r"\b(\d+)\s*h(?:rs?)?\s+(?:a|per)\s+(?:day|week)\b", re.I),
]

_LEVEL_KEYWORDS: dict[str, list[str]] = {
    "beginner": [
        "beginner", "newbie", "new to", "no experience", "never used",
        "starting from scratch", "zero knowledge", "complete beginner",
        "total beginner", "first time",
    ],
    "intermediate": [
        "intermediate", "some experience", "familiar with", "basic knowledge",
        "worked with", "know the basics", "moderate", "decent understanding",
    ],
    "advanced": [
        "advanced", "experienced", "expert", "professional", "years of experience",
        "senior", "proficient", "deep knowledge", "well-versed",
    ],
}


class ProfileAgent(BaseAgent):
    """Extract structured learner profile data from plain text.

    Uses lightweight regular expressions and keyword matching —
    no LLM call needed — so responses are instant and deterministic.

    The extracted dict is intended as shared context passed to
    :class:`~app.agents.planner_agent.PlannerAgent` and
    :class:`~app.agents.resource_agent.ResourceAgent`.

    Example::

        agent = ProfileAgent()
        profile = agent.extract("I want to learn Python in 3 months, 2h/day")
        # {
        #   "goal": "Python",
        #   "timeline": "3 months",
        #   "experience_level": "unknown",
        #   "study_hours": "2",
        # }
    """

    # ------------------------------------------------------------------
    # BaseAgent contract
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Return the agent identifier."""
        return "ProfileAgent"

    @property
    def description(self) -> str:
        """Return a one-line summary."""
        return (
            "Extracts learner goal, timeline, experience level, "
            "and study hours from free-form text without an AI call."
        )

    def process(self, user_input: str) -> str:
        """Extract a profile and return a human-readable summary.

        This method satisfies the :class:`~app.agents.base_agent.BaseAgent`
        contract so the coordinator can call ``process()`` uniformly.
        For programmatic use, prefer :meth:`extract` which returns a dict.

        Args:
            user_input: Raw text from the user.

        Returns:
            str: A formatted plain-text summary of the extracted profile.

        Raises:
            ValueError: If ``user_input`` is blank.
        """
        self._validate(user_input)
        profile = self.extract(user_input)
        return self._format_profile(profile)

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def extract(self, text: str) -> dict[str, Any]:
        """Parse ``text`` and return a structured profile dictionary.

        Keys always present in the returned dict:

        * ``goal`` – detected learning target, or ``"not specified"``.
        * ``timeline`` – detected duration, or ``"not specified"``.
        * ``experience_level`` – ``"beginner"``, ``"intermediate"``,
          ``"advanced"``, or ``"unknown"``.
        * ``study_hours`` – detected weekly/daily hours, or ``"not specified"``.

        Args:
            text: Free-form user message to parse.

        Returns:
            dict[str, Any]: Structured learner profile.
        """
        return {
            "goal": self._extract_goal(text),
            "timeline": self._extract_timeline(text),
            "experience_level": self._extract_level(text),
            "study_hours": self._extract_hours(text),
        }

    # ------------------------------------------------------------------
    # Private extraction helpers
    # ------------------------------------------------------------------

    def _extract_goal(self, text: str) -> str:
        """Return the detected learning goal or ``'not specified'``."""
        for pattern in _GOAL_PATTERNS:
            match = pattern.search(text)
            if match:
                return match.group(1).strip().rstrip(".")
        return "not specified"

    def _extract_timeline(self, text: str) -> str:
        """Return the detected timeline or ``'not specified'``."""
        for pattern in _TIMELINE_PATTERNS:
            match = pattern.search(text)
            if match:
                return match.group(1).strip()
        return "not specified"

    def _extract_level(self, text: str) -> str:
        """Return the detected experience level or ``'unknown'``."""
        lower = text.lower()
        for level, keywords in _LEVEL_KEYWORDS.items():
            if any(kw in lower for kw in keywords):
                return level
        return "unknown"

    def _extract_hours(self, text: str) -> str:
        """Return the detected study-hours figure or ``'not specified'``."""
        for pattern in _HOURS_PATTERNS:
            match = pattern.search(text)
            if match:
                return match.group(1).strip()
        return "not specified"

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    @staticmethod
    def _format_profile(profile: dict[str, Any]) -> str:
        """Render a profile dict as a human-readable string."""
        lines = [
            "📋 Learner Profile",
            "-" * 40,
            f"  Goal            : {profile['goal']}",
            f"  Timeline        : {profile['timeline']}",
            f"  Experience Level: {profile['experience_level']}",
            f"  Study Hours     : {profile['study_hours']}",
            "-" * 40,
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _validate(text: str) -> None:
        """Raise ValueError for blank input."""
        if not text or not text.strip():
            raise ValueError("user_input must not be empty.")
