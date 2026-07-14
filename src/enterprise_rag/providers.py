"""
providers.py — One function, four LLM providers. The routing layer.

WHY THIS FILE EXISTS (this is the skill you said you wanted)
------------------------------------------------------------
You asked: "how do I learn when to use the right model at the right
level?" The answer starts architecturally: NEVER let provider-specific
code leak into your business logic. generation.py calls chat() and has
no idea which company is behind it. That means switching providers is a
one-line .env change — and comparing them becomes an experiment, not a
rewrite.

THE ROUTING MENTAL MODEL (memorize this, it's an interview answer):
  • Dev loop / high-volume / private data → LOCAL (Ollama on your Mac mini)
  • Production answers, cost-sensitive    → SMALL API model (gpt-4o-mini, haiku)
  • Judging, complex reasoning, evals     → BIGGER model (sonnet, gpt-4o)
  • Enterprise/AWS-native requirement     → BEDROCK (same models, AWS billing,
                                            IAM auth, VPC isolation — the
                                            reasons enterprises pay for it)

DESIGN NOTE ▸ imports happen INSIDE each function ("lazy imports") so you
only need the SDK for the provider you actually use. requirements.txt
keeps the others commented out for the same reason.

TRY IT YOURSELF FIRST ▸ Write your own chat(messages) that just calls
Ollama with the `requests` library (its API is one POST). Get that
working end-to-end before reading the other three branches here.
"""

from src.config import get_settings

# A message is a plain dict: {"role": "system"|"user"|"assistant", "content": str}
# We use the raw dict format because every provider speaks some dialect of it.


def chat(messages: list[dict], max_tokens: int = 700, temperature: float = 0.1) -> str:
    """Route a chat request to whichever provider .env selects.

    WHY temperature=0.1: RAG answers should be grounded and repeatable,
    not creative. Low temperature = less variance = easier to evaluate.
    (Creative writing wants 0.8+; grounded Q&A wants ~0-0.2.)
    """
    provider = get_settings().llm_provider.lower()
    if provider == "ollama":
        return _ollama(messages, max_tokens, temperature)
    if provider == "openai":
        return _openai(messages, max_tokens, temperature)
    if provider == "anthropic":
        return _anthropic(messages, max_tokens, temperature)
    if provider == "bedrock":
        return _bedrock(messages, max_tokens, temperature)
    raise ValueError(
        f"Unknown LLM_PROVIDER '{provider}'. Use: ollama | openai | anthropic | bedrock"
    )


def _ollama(messages: list[dict], max_tokens: int, temperature: float) -> str:
    """Local models via Ollama's HTTP API. Free. Private. Your dev loop.

    COMMON BUG: forgetting `ollama serve` is not running, or the model
    isn't pulled (`ollama pull llama3.1`). The ConnectionError below is
    almost always that.
    """
    import requests

    s = get_settings()
    resp = requests.post(
        f"{s.ollama_url}/api/chat",
        json={
            "model": s.ollama_model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def _openai(messages: list[dict], max_tokens: int, temperature: float) -> str:
    from openai import OpenAI  # lazy import — only needed if you use it

    s = get_settings()
    client = OpenAI(api_key=s.openai_api_key)
    resp = client.chat.completions.create(
        model=s.openai_model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content


def _anthropic(messages: list[dict], max_tokens: int, temperature: float) -> str:
    """NOTE the API-shape difference: Anthropic takes `system` as its own
    parameter, not as a message. This is exactly why the abstraction layer
    exists — callers never deal with these dialect differences."""
    from anthropic import Anthropic

    s = get_settings()
    system = "\n".join(m["content"] for m in messages if m["role"] == "system")
    convo = [m for m in messages if m["role"] != "system"]
    client = Anthropic(api_key=s.anthropic_api_key)
    resp = client.messages.create(
        model=s.anthropic_model,
        system=system or None,
        messages=convo,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.content[0].text


def _bedrock(messages: list[dict], max_tokens: int, temperature: float) -> str:
    """AWS Bedrock via the Converse API — your $80 credits path.

    INTERVIEW NOTE: Bedrock's value isn't the models (same ones you get
    direct). It's IAM-based auth (no API keys to leak), CloudWatch logging,
    VPC endpoints, and one bill inside AWS. That sentence IS the answer to
    "why would an enterprise use Bedrock?"

    AUTH: boto3 reads credentials from `aws configure` / env vars — that's
    IAM in action; notice there's no api_key parameter anywhere below.
    """
    import boto3

    s = get_settings()
    client = boto3.client("bedrock-runtime", region_name=s.aws_region)
    system = [{"text": m["content"]} for m in messages if m["role"] == "system"]
    convo = [
        {"role": m["role"], "content": [{"text": m["content"]}]}
        for m in messages
        if m["role"] != "system"
    ]
    resp = client.converse(
        modelId=s.bedrock_model_id,
        system=system or None,
        messages=convo,
        inferenceConfig={"maxTokens": max_tokens, "temperature": temperature},
    )
    return resp["output"]["message"]["content"][0]["text"]
