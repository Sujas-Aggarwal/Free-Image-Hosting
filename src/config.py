from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

class Config:
    API_KEYS = {
        "FREEIMAGEHOST_API_KEY": os.getenv("FREEIMAGEHOST_API_KEY")
    }
