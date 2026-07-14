"""
config.py — One typed object that owns all settings.

WHY THIS FILE EXISTS
--------------------
Beginners scatter os.getenv() calls everywhere. Then a typo in an env var
name fails silently at runtime, in production, at 2am. pydantic-settings
loads .env ONCE into a validated object — wrong types or missing values
fail loudly at startup instead. In an interview this is called
"fail-fast configuration."

LEARN CHECKPOINT ▸ Before reading on: what happens if TOP_K is set to
"five" instead of 5 in .env? Answer: pydantic raises a ValidationError
at import time. With raw os.getenv you'd get a string "five" and a
confusing crash deep inside retrieval. That difference is the whole
argument for this file.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Provider routing — this one string decides which LLM answers questions.
    llm_provider: str = "ollama"  # ollama | openai | anthropic | bedrock

    # Ollama (local, free — your Mac mini)
    ollama_model: str = "llama3.1"
    ollama_url: str = "http://localhost:11434"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Anthropic
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-haiku-4-5"

    # AWS Bedrock (your $80 credits live here — this is the v2 path)
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "anthropic.claude-3-5-haiku-20241022-v1:0"

    # Retrieval
    top_k: int = 5
    chroma_dir: str = "chroma_db"

    # Embeddings — small, fast, runs locally. See docs/tool_selection_playbook.md
    # for how to choose an embedding model (hint: MTEB leaderboard on Hugging Face).
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """lru_cache = read .env once, reuse everywhere. A tiny singleton pattern.

    INTERVIEW NOTE: if asked "how do you manage configuration?", the answer
    is: typed settings object, loaded from environment, validated at startup,
    never hard-coded secrets. This function is that answer in 3 lines.
    """
    return Settings()
