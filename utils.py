import os
from dotenv import load_dotenv

def load_environment_variables():
    """
    Loads and returns the environment variables required for the application.

    Returns:
        dict: A dictionary with environment variable names as keys and their values.
    """
    load_dotenv()
    
    return {
        "SERPER_API_KEY": os.getenv("SERPER_API_KEY"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPENAI_MODEL_NAME": os.getenv("OPENAI_MODEL_NAME"),
        "OPENAI_API_BASE": os.getenv("OPENAI_API_BASE"),
    }