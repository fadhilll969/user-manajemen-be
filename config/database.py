import os
from dotenv import load_dotenv
from pony.orm import Database

load_dotenv()

db = Database()

db.bind(
    provider="mysql",
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME")
)