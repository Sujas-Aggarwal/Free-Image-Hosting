from dotenv import load_dotenv
import os
from src.cli import CLIInterface
from config import Config  # Import Config if needed here

# Load the .env file early
load_dotenv()

if __name__ == "__main__":
    cli = CLIInterface()
    cli.start()
