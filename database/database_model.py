from sqlalchemy import create_engine
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(override=True)
don_env = find_dotenv()

database_url = os.environ["database_url"]
engine = create_engine(database_url)