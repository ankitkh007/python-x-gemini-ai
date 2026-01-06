import os
from dotenv import load_dotenv
from google import genai

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

prompt = input("Enter any promt: ")
response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

print(response.text)
