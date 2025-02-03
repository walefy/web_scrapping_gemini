import os
from google import genai
from pathlib import Path
from google.genai import types
from pydantic import ValidationError
from src.model import AIResponse


class AIService:
    _client: genai.Client
    _default_prompt: str


    def __init__(self, agent: str):
        GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

        if not GEMINI_API_KEY:
            raise ValueError('require GEMINI_API_KEY env')

        self._client = genai.Client(api_key=GEMINI_API_KEY)
        self._default_prompt = agent


    def ask(self, question: str) -> AIResponse:
        response: str | None = ''

        try:
            response = self._client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=types.Part.from_text(text=question),
                config=types.GenerateContentConfig(
                    system_instruction=self._default_prompt,
                    response_mime_type="application/json",
                    response_schema=AIResponse,
                )
            ).text
        except:
            raise ValueError('Gemini service error!')

        if not response:
            raise ValueError('Gemini service error!')

        try:
            return AIResponse.model_validate_json(response)

        except ValidationError as e:
            raise ValueError(f"Response validation error: {e}")
