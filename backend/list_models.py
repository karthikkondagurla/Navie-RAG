import os
import google.generativeai as genai
from dotenv import load_dotenv; load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("No API Key found in .env")
    exit(1)

genai.configure(api_key=api_key)

print("Listing available models...")
try:
    with open("backend/clean_models.txt", "w", encoding="utf-8") as f:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
    print("Models written to backend/clean_models.txt")
except Exception as e:
    print(f"Error listing models: {e}")
