import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("API KEY NOT FOUND!!")
