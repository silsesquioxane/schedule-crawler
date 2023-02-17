import os

from dotenv import load_dotenv

load_dotenv()
ENV_VARS = dict(os.environ)
user_id = ENV_VARS["USER_ID"]
password = ENV_VARS["PASSWORD"]
