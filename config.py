"""Configuration centralisée de Volt Explorer.

Les valeurs sensibles (clés API) viennent UNIQUEMENT de variables d'environnement
(fichier .env en local, jamais versionné). Elles ne sont jamais envoyées au navigateur.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    JSON_AS_ASCII = False

    DATA_DIR = BASE_DIR / "data"
   # Sur Vercel, utiliser le dossier temporaire accessible en écriture.
if os.getenv("VERCEL"):
    DATABASE = "/tmp/volt_explorer.sqlite3"
else:
    DATABASE = os.getenv(
        "DATABASE_PATH",
        str(BASE_DIR / "database" / "volt_explorer.sqlite3")
    )
    PROPOSITIONS_JSON = str(DATA_DIR / "propositions.json")
    QUIZ_JSON = str(DATA_DIR / "quiz.json")
    PROGRAMME_PDF = str(DATA_DIR / "programme.pdf")  # optionnel : voir README

    # --- Assistant IA ---
    # demo (par défaut, sans clé) | anthropic | openai
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "demo").lower()
    LLM_MODEL = os.getenv("LLM_MODEL", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    RAG_TOP_K = int(os.getenv("RAG_TOP_K", "4"))
    RAG_MIN_SCORE = float(os.getenv("RAG_MIN_SCORE", "0.08"))
    LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "30"))


class TestConfig(Config):
    TESTING = True
    LLM_PROVIDER = "demo"
