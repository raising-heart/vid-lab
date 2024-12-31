import os
import google.generativeai as genai
from dotenv import load_dotenv

def configure_api_direct():
    """
    Load API key from .env file
    Make sure to create a .env file with your GEMINI_API_KEY
    """
    # Load environment variables from .env file
    load_dotenv()
    
    API_KEY = os.getenv('GEMINI_API_KEY')
    if not API_KEY:
        raise ValueError("No API key found. Please set GEMINI_API_KEY in your .env file")
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel(model_name='gemini-1.5-flash-latest')
