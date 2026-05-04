from config import get_settings
from models import ClassificationResult
import json


class LLMClassifier:
    def __init__(self):
        settings = get_settings()
        self.provider = settings.llm_provider

        if self.provider == "anthropic":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=settings.anthropic_api_key)
        elif self.provider == "google":
            import google.generativeai as genai
            genai.configure(api_key=settings.google_api_key)
            self.client = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

    def _get_classification_prompt(self, text: str) -> str:
        return f"""Analyze this input and classify it into a structured format.

Input: "{text}"

Determine:
1. Is this a GOAL (multi-week, broader ambition, not immediately actionable) or a TASK (concrete, completable action)?
2. What category does it belong to? Choose from: chore, wish, upgrade, health, work, personal, learning, social, finance, other
3. What's the timeline? Choose from: today, this_week, this_month, bucket
4. Extract a clear, concise title (max 80 chars)
5. If there's additional context, put it in description
6. If there's a deadline mentioned, extract it as loose_deadline (e.g., "by end of week", "tomorrow", "next Monday")
7. If it's a GOAL, suggest 2-3 concrete starter tasks

Respond ONLY with valid JSON in this exact format:
{{
    "item_type": "goal" or "task",
    "category": "category_name",
    "timeline": "today/this_week/this_month/bucket",
    "title": "clear title",
    "description": "additional context or null",
    "loose_deadline": "extracted deadline or null",
    "suggested_tasks": ["task1", "task2"] or null (only for goals)
}}"""

    def _classify_with_anthropic(self, text: str) -> str:
        prompt = self._get_classification_prompt(text)
        message = self.client.messages.create(
            model="claude-haiku-4.0-20250604",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return message.content[0].text.strip()

    def _classify_with_google(self, text: str) -> str:
        prompt = self._get_classification_prompt(text)
        response = self.client.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 500,
            }
        )
        return response.text.strip()

    def classify(self, text: str) -> ClassificationResult:
        try:
            if self.provider == "anthropic":
                response_text = self._classify_with_anthropic(text)
            elif self.provider == "google":
                response_text = self._classify_with_google(text)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")

            # Parse JSON response
            classification_data = json.loads(response_text)
            return ClassificationResult(**classification_data)

        except (json.JSONDecodeError, Exception) as e:
            # Fallback classification if LLM fails
            print(f"Classification error: {e}")
            return ClassificationResult(
                item_type="task",
                category="other",
                timeline="bucket",
                title=text[:80],
                description=text if len(text) > 80 else None
            )
