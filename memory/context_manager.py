"""
memory/context_manager.py
-------------------------

High-level context manager for the Learning Roadmap Concierge AI.

Provides convenient methods for reading and updating
conversation context without directly interacting with
MemoryManager.
"""

from memory.memory_manager import MemoryManager


class ContextManager:
    """
    High-level wrapper around MemoryManager.

    Agents should use this class instead of directly
    accessing MemoryManager.
    """

    def __init__(self):

        self.memory = MemoryManager()

    # ---------------------------------------------

    def initialize(self, session_id: str):

        self.memory.initialize_context(session_id)

    # ---------------------------------------------

    def get(self, session_id: str):

        return self.memory.get_context(session_id)

    # ---------------------------------------------

    def update(self, session_id: str, **kwargs):

        self.memory.update_context(session_id, **kwargs)

    # ---------------------------------------------

    def clear(self, session_id: str):

        self.memory.clear_context(session_id)

    # ---------------------------------------------
    # Goal
    # ---------------------------------------------

    def goal(self, session_id: str):

        return self.get(session_id).get("goal")

    def set_goal(self, session_id: str, goal: str):

        self.update(session_id, goal=goal)

    # ---------------------------------------------
    # Current Topic
    # ---------------------------------------------

    def current_topic(self, session_id: str):

        return self.get(session_id).get("current_topic")

    def set_current_topic(
        self,
        session_id: str,
        topic: str,
    ):

        self.update(session_id, current_topic=topic)

    # ---------------------------------------------
    # Completed Topics
    # ---------------------------------------------

    def completed_topics(self, session_id: str):

        return self.get(session_id).get("completed_topics")

    def set_completed_topics(
        self,
        session_id: str,
        topics: list,
    ):

        self.update(
            session_id,
            completed_topics=topics,
        )

    # ---------------------------------------------
    # Remaining Topics
    # ---------------------------------------------

    def remaining_topics(self, session_id: str):

        return self.get(session_id).get("remaining_topics")

    def set_remaining_topics(
        self,
        session_id: str,
        topics: list,
    ):

        self.update(
            session_id,
            remaining_topics=topics,
        )

    # ---------------------------------------------
    # Last Agent
    # ---------------------------------------------

    def last_agent(self, session_id: str):

        return self.get(session_id).get("last_agent")

    def set_last_agent(
        self,
        session_id: str,
        agent: str,
    ):

        self.update(
            session_id,
            last_agent=agent,
        )

    # ---------------------------------------------
    # Last Action
    # ---------------------------------------------

    def last_action(self, session_id: str):

        return self.get(session_id).get("last_action")

    def set_last_action(
        self,
        session_id: str,
        action: str,
    ):

        self.update(
            session_id,
            last_action=action,
        )