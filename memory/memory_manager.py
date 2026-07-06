"""
memory/memory_manager.py
------------------------

Thread-safe, in-process session memory for the Learning Roadmap
Concierge AI.

MemoryManager stores arbitrary key-value pairs grouped by session ID.
Multiple sessions are fully isolated from one another. All public
methods acquire a shared ``threading.Lock`` before touching the
internal store, making the class safe to use from concurrent threads
(e.g., a future async web server or parallel test runners).

Data model::

    _store = {
        "<session_id>": {
            "<key>": <value>,
            ...
        },
        ...
    }

Notes
-----
* All state is in-memory only and lost when the process exits.
* To add persistence, replace the ``_store`` read/write paths with
  calls to a database or file backend — the public API stays the same.
"""

import threading
from typing import Any


class MemoryManager:
    """
    Thread-safe, session-scoped in-memory key-value store.

    Each session is an isolated namespace: two different session IDs
    never see each other's data even if they use the same key names.

    All mutations and reads are protected by a single
    :class:`threading.Lock`, so the class is safe for use from
    multiple threads without external synchronisation.

    Example::

        mm = MemoryManager()

        mm.save("s1", "goal", "Learn Python")
        mm.save("s1", "turn", 1)

        print(mm.load("s1", "goal"))        # "Learn Python"
        print(mm.load_all("s1"))            # {"goal": "Learn Python", "turn": 1}
        print(mm.has("s1", "turn"))         # True

        mm.delete("s1", "turn")
        print(mm.has("s1", "turn"))         # False

        mm.clear("s1")
        print(mm.load_all("s1"))            # {}
    """
    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self) -> None:

        if hasattr(self, "_initialized"):
            return

        self._store = {}

        self._lock = threading.Lock()

        self._initialized = True

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def save(self, session_id: str, key: str, value: Any) -> None:
        """Persist ``value`` under ``key`` for ``session_id``.

        Creates the session namespace automatically if it does not
        already exist.

        Args:
            session_id: Unique identifier for the conversation session.
            key:        Arbitrary string label for the stored value.
            value:      Any Python object to store.

        Raises:
            ValueError: If ``session_id`` or ``key`` are blank strings.
        """
        self._validate_ids(session_id, key)
        with self._lock:
            self._ensure_session(session_id)
            self._store[session_id][key] = value

    def load(self, session_id: str, key: str) -> Any | None:
        """Return the value stored at ``key`` for ``session_id``.

        Returns ``None`` if either the session or the key does not
        exist, rather than raising an exception.  Callers that need
        to distinguish "not set" from ``None`` should use :meth:`has`
        before calling this method.

        Args:
            session_id: Unique identifier for the conversation session.
            key:        Key to look up.

        Returns:
            The stored value, or ``None`` if not found.

        Raises:
            ValueError: If ``session_id`` or ``key`` are blank strings.
        """
        self._validate_ids(session_id, key)
        with self._lock:
            return self._store.get(session_id, {}).get(key)

    def load_all(self, session_id: str) -> dict[str, Any]:
        """Return a shallow copy of all key-value pairs for ``session_id``.

        Returns an empty dict when the session has no data, so callers
        never need to guard against ``None``.

        Args:
            session_id: Unique identifier for the conversation session.

        Returns:
            dict[str, Any]: Copy of the session's memory store.

        Raises:
            ValueError: If ``session_id`` is a blank string.
        """
        self._validate_session_id(session_id)
        with self._lock:
            return dict(self._store.get(session_id, {}))

    def delete(self, session_id: str, key: str) -> None:
        """Remove ``key`` from ``session_id``'s namespace.

        Is a no-op if the session or key does not exist.

        Args:
            session_id: Unique identifier for the conversation session.
            key:        Key to remove.

        Raises:
            ValueError: If ``session_id`` or ``key`` are blank strings.
        """
        self._validate_ids(session_id, key)
        with self._lock:
            if session_id in self._store:
                self._store[session_id].pop(key, None)

    def clear(self, session_id: str) -> None:
        """Remove all keys for ``session_id``.

        The session namespace itself is deleted so
        :meth:`load_all` returns ``{}`` afterwards.  Is a no-op if
        the session does not exist.

        Args:
            session_id: Unique identifier for the conversation session.

        Raises:
            ValueError: If ``session_id`` is a blank string.
        """
        self._validate_session_id(session_id)
        with self._lock:
            self._store.pop(session_id, None)

    def has(self, session_id: str, key: str) -> bool:
        """Return ``True`` if ``key`` exists in ``session_id``'s namespace.

        Distinguishes between a missing key and a key explicitly set to
        ``None`` — both :meth:`load` cases return ``None``, but only a
        truly missing key returns ``False`` here.

        Args:
            session_id: Unique identifier for the conversation session.
            key:        Key to check.

        Returns:
            bool: ``True`` if the key exists, ``False`` otherwise.

        Raises:
            ValueError: If ``session_id`` or ``key`` are blank strings.
        """
        self._validate_ids(session_id, key)
        with self._lock:
            return key in self._store.get(session_id, {})
    # ------------------------------------------------------------------
    # Context Management
    # ------------------------------------------------------------------

    def initialize_context(self, session_id: str) -> None:
        """
        Initialize structured session context.
        """

        self._validate_session_id(session_id)

        with self._lock:

            self._ensure_session(session_id)

            if "context" not in self._store[session_id]:

                self._store[session_id]["context"] = {

                    "goal": None,

                    "current_topic": None,

                    "completed_topics": [],

                    "remaining_topics": [],

                    "last_agent": None,

                    "last_action": None,

                }

    def get_context(self, session_id: str) -> dict:
        """
        Return structured session context.
        """

        self.initialize_context(session_id)

        with self._lock:

            return dict(self._store[session_id]["context"])

    def update_context(
        self,
        session_id: str,
        **kwargs,
    ) -> None:
        """
        Update selected context values.
        """

        self.initialize_context(session_id)

        with self._lock:

            self._store[session_id]["context"].update(kwargs)

    def clear_context(self, session_id: str) -> None:
        """
        Reset structured session context.
        """

        self.initialize_context(session_id)

        with self._lock:

            self._store[session_id]["context"] = {

                "goal": None,

                "current_topic": None,

                "completed_topics": [],

                "remaining_topics": [],

                "last_agent": None,

                "last_action": None,

            }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _ensure_session(self, session_id: str) -> None:
        """Create the session namespace if it is absent.

        Must be called **inside** the lock.

        Args:
            session_id: Session to initialise.
        """
        if session_id not in self._store:
            self._store[session_id] = {}

    @staticmethod
    def _validate_ids(session_id: str, key: str) -> None:
        """Raise ValueError if either identifier is blank.

        Args:
            session_id: Session identifier to validate.
            key:        Key identifier to validate.

        Raises:
            ValueError: On blank ``session_id`` or ``key``.
        """
        MemoryManager._validate_session_id(session_id)
        if not key or not key.strip():
            raise ValueError("'key' must not be empty or blank.")

    @staticmethod
    def _validate_session_id(session_id: str) -> None:
        """Raise ValueError if the session identifier is blank.

        Args:
            session_id: Session identifier to validate.

        Raises:
            ValueError: On blank ``session_id``.
        """
        if not session_id or not session_id.strip():
            raise ValueError("'session_id' must not be empty or blank.")
