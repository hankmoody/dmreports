import os
from dotenv import load_dotenv, find_dotenv

# Find the .env file
env_path = find_dotenv()

if not env_path:
  raise FileNotFoundError(".env file not found")
load_dotenv()

def get_secret(name: str):
  return os.getenv(name)