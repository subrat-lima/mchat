import os

from dotenv import load_dotenv

load_dotenv()
assert os.getenv("SECRET_KEY")
