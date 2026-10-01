import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # FIXED: Explicitly set to the latest stable model as recommended by Google API
    MODEL_NAME = "gemini-2.5-Pro"  