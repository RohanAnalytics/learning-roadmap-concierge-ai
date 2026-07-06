"""
model.py
--------

Initializes and exposes a reusable Google GenAI client.

Responsibilities
----------------
- Load environment variables from the project's .env file.
- Read the Google API Key.
- Read the model name from the environment.
- Create a single reusable Gemini client.
- Provide helper functions used by all AI agents.
"""

from config.constants import DEFAULT_MODEL
from pathlib import Path
import os

from dotenv import load_dotenv
from google import genai
import streamlit as st

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

# ----------------------------------------------------
# Configuration
# ----------------------------------------------------

API_KEY = (
    os.getenv("GOOGLE_API_KEY")
    or st.secrets.get("GOOGLE_API_KEY")
)

MODEL_NAME = (
    os.getenv("MODEL_NAME")
    or st.secrets.get("MODEL_NAME", DEFAULT_MODEL)
)

if not API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY is missing. Configure it locally in .env "
        "or add it as a Streamlit Community Cloud Secret."
    )

# ----------------------------------------------------
# Singleton Client
# ----------------------------------------------------

_client = None


def get_client() -> genai.Client:
    """
    Return a reusable Google GenAI client.

    The client is created only once (Singleton Pattern),
    allowing every AI agent to share the same connection.
    """

    global _client

    if _client is None:
        _client = genai.Client(api_key=API_KEY)

    return _client


def get_model_name() -> str:
    """
    Return the configured Gemini model name.
    """

    return MODEL_NAME