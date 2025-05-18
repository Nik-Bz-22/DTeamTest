from google import genai
from django.conf import settings

# import json
import ast


def ai_translate(json_data: dict, target_language: str) -> dict[str, str] | None:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""
            Translate the following json to {target_language} don't translate json keys and as a result give me ONLY json.
            Without any other test and content. After thet i want to load it in python with json.load: {json_data}""",
        )
        clear_data = response.text.split("```json")[1].split("```")[0].strip()
        json_result = ast.literal_eval(clear_data)

        return json_result
    except Exception:
        return None
