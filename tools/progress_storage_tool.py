import json
import os
from threading import Lock
from pathlib import Path

class ProgressStorageTool:
    """
    Pure storage layer for learning progress tracking.
    No AI logic. Only JSON read/write operations.
    """

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent

        self.file_path = BASE_DIR / "data" / "progress.json"

        self.lock = Lock()

        self._ensure_file_exists()

    # -------------------------
    # Internal Helper
    # -------------------------
    def _ensure_file_exists(self):
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, "w") as f:
                json.dump({"users": {}}, f, indent=2)

    def _read(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # -------------------------
    # Public APIs
    # -------------------------

    def load_progress(self):
        """Return full progress file"""
        with self.lock:
            return self._read()

    def save_progress(self, data):
        """Overwrite entire progress file"""
        with self.lock:
            self._write(data)

    def get_progress(self, user: str):
        """Get progress for a specific user"""
        with self.lock:
            data = self._read()
            return data.get("users", {}).get(user, {})

    def mark_completed(self, user: str, course: str, topic: str):
        """
        Mark a topic as completed for a user under a course.
        Automatically creates structure if missing.
        """
        with self.lock:
            data = self._read()

            if "users" not in data:
                data["users"] = {}

            if user not in data["users"]:
                data["users"][user] = {}

            if course not in data["users"][user]:
                data["users"][user][course] = {
                    "completed": [],
                    "remaining": []
                }

            user_course = data["users"][user][course]

            # Check if already completed
            for completed_topic in user_course["completed"]:
                if completed_topic.lower() == topic.lower():
                    return "already_completed"

            # Find the actual topic stored in remaining
            actual_topic = None
            for remaining_topic in user_course["remaining"]:
                if remaining_topic.lower() == topic.lower():
                    actual_topic = remaining_topic
                    break

            if actual_topic:

                user_course["completed"].append(actual_topic)
                user_course["remaining"].remove(actual_topic)

                self._write(data)

                return user_course

            return "topic_not_found"

    def reset_progress(self, user: str):
        """Delete all progress for a user"""
        with self.lock:
            data = self._read()

            if "users" in data and user in data["users"]:
                data["users"][user] = {}

            self._write(data)