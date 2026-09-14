from ..LLMInterface import LLMInterface
from ..LLMEnums import GeminiEnums
import google.generativeai as genai
import logging
from typing import List, Union

class GeminiProvider(LLMInterface):

    def __init__(self, api_key: str,
                       default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):

        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        genai.configure(api_key=self.api_key)

        self.enums = GeminiEnums
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):

        if not self.generation_model_id:
            self.logger.error("Generation model for Gemini was not set")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        # Gemini لا يدعم role="system" داخل contents، لازم يمر عبر system_instruction
        system_instruction = None
        filtered_history = []

        for message in chat_history:
            if message.get("role") == GeminiEnums.SYSTEM.value:
                # ندمج كل نصوص الـ system في system_instruction واحد
                system_text = " ".join(message.get("parts", []))
                system_instruction = (
                    f"{system_instruction} {system_text}".strip()
                    if system_instruction else system_text
                )
            else:
                filtered_history.append(message)

        model = genai.GenerativeModel(
            self.generation_model_id,
            system_instruction=system_instruction,
        )

        contents = filtered_history + [
            self.construct_prompt(prompt=prompt, role=GeminiEnums.USER.value)
        ]

        response = model.generate_content(
            contents=contents,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
            ),
        )

        if not response or not response.text:
            self.logger.error("Error while generating text with Gemini")
            return None

        return response.text

    def embed_text(self, text: Union[str, List[str]], document_type: str = None):

        if not self.embedding_model_id:
            self.logger.error("Embedding model for Gemini was not set")
            return None

        if isinstance(text, str):
            text = [text]

        task_type = "retrieval_document"
        if document_type == "query":
            task_type = "retrieval_query"

        embeddings = []
        for t in text:
            response = genai.embed_content(
                model=self.embedding_model_id,
                content=self.process_text(t),
                task_type=task_type,
            )
            if not response or "embedding" not in response:
                self.logger.error("Error while embedding text with Gemini")
                return None
            embeddings.append(response["embedding"])

        return embeddings

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "parts": [prompt],
        }