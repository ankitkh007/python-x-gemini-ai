from core.gemini_client import client
from google.genai import types
from PIL import Image

# prompt = input("Enter any promt: ")

## Testing Systeminstructions, temperature
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=prompt,
#     config=types.GenerateContentConfig(
#         system_instruction="Response should be within 50 words. Your resposes should be like sigma male.",
#         temperature=0.5,
#     ),
# )


## Testing Multimodal response
# image = Image.open("projects\images\sigma_boys.jpeg")
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=[image, "Describe this image."],
#     config=types.GenerateContentConfig(
#         system_instruction="Response should be within 50 words. "
#         "Respond like you're roasting the subjects."
#         "No mercy Pure Roasting!",
#         temperature=0.5,
#     ),
# )

# print("Gemini response: ")
# print("----------------------------------------")
# print(response.text)

## Testing Streaming responses
response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Explain how AI works!",
    config=types.GenerateContentConfig(
        system_instruction="Response should be within 500 words. ",
        temperature=0.5,
    ),
)

for chunk in response:
    print(chunk.text, end="------------")
