from core.gemini_client import client
from google.genai import types

grounding_tool = types.Tool(google_search=types.GoogleSearch())

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Who won euro 2024?",
    config=types.GenerateContentConfig(
        system_instruction="Response should be within 20 words", tools=[grounding_tool]
    ),
)

print(response.text)
