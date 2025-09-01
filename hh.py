# test_env.py
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"✅ OpenAI API Key found: {api_key}...")
else:
    print("❌ OpenAI API Key NOT found! Check your .env file")