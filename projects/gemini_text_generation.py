from core.gemini_client import client
from google.genai import types

prompt = input("Enter any promt: ")

## Testing Systeminstructions
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction="Response should be within 50 words. Your resposes should be like sigma male.",
        temperature=0.5,
    ),
)

print("Gemini response: ")
print("----------------------------------------")
print(response.text)
