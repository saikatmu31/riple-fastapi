# core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
    API_KEY = os.getenv("API_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    MODEL_PATH = os.getenv("MODEL_PATH")

config = Config()

