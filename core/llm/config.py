import os


class LLMConfig:
    def __init__(self):
        self.default_provider = os.getenv("LLM_DEFAULT_PROVIDER", "gemini")
        self.default_model = os.getenv("LLM_DEFAULT_MODEL", "")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "4096"))
        self.timeout_seconds = float(os.getenv("LLM_TIMEOUT_SECONDS", "60"))


llm_config = LLMConfig()