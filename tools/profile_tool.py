"""
tools/profile_tool.py
---------------------

Profile Tool

Handles reading and writing user profiles
stored in data/user_profiles.json.
"""

from __future__ import annotations

import json
from pathlib import Path


class ProfileTool:
    """Handles user profile storage."""

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent
        self.file_path = BASE_DIR / "data" / "user_profiles.json"

        if not self.file_path.exists():

            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            self.file_path.write_text(
                "{}",
                encoding="utf-8",
            )

        else:

            if self.file_path.stat().st_size == 0:

                self.file_path.write_text(
                    "{}",
                    encoding="utf-8",
                )

    def load_profiles(self) -> dict:
        """Load all user profiles."""

        try:

            return json.loads(
                self.file_path.read_text(encoding="utf-8")
                )
        except (json.JSONDecodeError, OSError):

            return {}

    def save_profiles(
        self,
        profiles: dict,
    ) -> None:
        """Save all user profiles."""

        self.file_path.write_text(
            json.dumps(
                profiles,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def get_profile(
        self,
        username: str,
    ) -> dict:
        """Return a user profile."""

        profiles = self.load_profiles()

        return profiles.get(username, {})

    def save_profile(
        self,
        username: str,
        profile: dict,
    ) -> None:
        """Save a single user profile."""

        profiles = self.load_profiles()

        profiles[username] = profile

        self.save_profiles(profiles)

    def update_profile(
        self,
        username: str,
        updates: dict,
    ) -> None:
        """Update specific fields of a user profile."""

        profiles = self.load_profiles()

        profile = profiles.setdefault(username, {})

        profile.update(updates)

        profiles[username] = profile

        self.save_profiles(profiles)

    def get_learning_context(
        self,
        username: str,
    ) -> str:
        """
        Return a formatted learner profile for AI prompts.
        """

        profile = self.get_profile(username)

        if not profile:
            return "No learner profile available."

        skills = profile.get("skills", [])
        completed = profile.get("completed_topics", 0)
        total = profile.get("total_topics", 0)

        return f"""
Learner Profile

Goal:
{profile.get("goal", "Unknown")}

Current Level:
{profile.get("current_level", "Unknown")}

Recommended Level:
{profile.get("recommended_level", "Unknown")}

Known Skills:
{", ".join(skills) if skills else "None"}

Missing Skills:
{", ".join(profile.get("missing_skills", [])) or "Unknown"}

Progress:
{completed}/{total} topics completed
Completion:
{round((completed/total)*100) if total else 0}%
"""