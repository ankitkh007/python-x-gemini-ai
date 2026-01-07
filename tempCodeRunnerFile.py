import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API KEY NOT FOUND!")

client = genai.Client(api_key=API_KEY)

prompt = input("Enter any promt: ")
response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

print("Gemini response: ")
print("----------------------------------------")
print(response.text)
