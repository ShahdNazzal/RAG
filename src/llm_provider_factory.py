import os
import requests


class OllamaClient:
    def __init__(self, base_url, model):
        self.base_url = base_url
        self.model = model

    def set_generation_model(self, model_id):
        self.model = model_id

    def generate(self, prompt):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()


class OpenAIClient:
    def __init__(self):
        pass


class LLMProviderFactory:
    def create(self, provider: str):
        provider = provider.lower()

        if provider == "ollama":
            return OllamaClient(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                model=os.getenv("GENERATION_MODEL_ID", "llama3.2")
            )

        elif provider == "openai":
            # dummy fallback (مش مستخدم عندك)
            return OpenAIClient()

        else:
            raise ValueError(f"Unknown LLM provider: {provider}")


llm_provider_factory = LLMProviderFactory()
