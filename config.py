import os
from dotenv import load_dotenv

ENV_FILE = ".env.test" if os.getenv("TEST_ENV") == "true" else ".env"
load_dotenv(ENV_FILE)
