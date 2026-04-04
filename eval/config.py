"""Model registry and configuration for DynToM evaluation."""

import os

# Data paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "script", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

# Trial range (paper uses 1,100 social contexts = trials 50-1149)
DEFAULT_TRIAL_START = 50
DEFAULT_TRIAL_END = 1150  # exclusive

# The user message sent after the system prompt (exact replica from old code)
REQUIRE_PROMPT = (
    'answer the 71 question, and response in JSON format:'
    '{[question_id]:[a, b, c or d], [question_id]:a, b, c or d, ...}. '
    'for example: {"type_d_how_1":"a","type_d_how_2":"b","type_d_how_3":"c"}'
)

# Model registry: name -> (provider, model_id)
MODELS = {
    "gpt-4-turbo": ("openai_chat", "gpt-4-turbo-2024-04-09"),
    "gpt-5.4": ("openai_responses", "gpt-5.4-2026-03-05"),
    "gpt-5.4-mini": ("openai_responses", "gpt-5.4-mini-2026-03-17"),
    "gpt-5.4-pro": ("openai_responses", "gpt-5.4-pro"),
    "gemini-3.1-pro": ("google", "gemini-3.1-pro-preview"),
    "claude-opus-4.6": ("anthropic", "claude-opus-4-6"),
}

# API keys from environment variables
def get_api_key(provider):
    env_map = {
        "openai_chat": "OPENAI_API_KEY",
        "openai_responses": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GEMINI_API_KEY",
    }
    var = env_map[provider]
    key = os.environ.get(var)
    if not key:
        raise ValueError(f"Environment variable {var} not set")
    return key
