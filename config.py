import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

load_dotenv()
TOKEN = os.getenv("TMDB_BEARER_TOKEN", "").strip()
PAGES = int(os.getenv("TMDB_PAGES", "5"))
BASE_URL = "https://api.themoviedb.org/3"

def get_engine():
    url = URL.create(
        "mysql+pymysql",
        username=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.getenv("MYSQL_DATABASE", "movie_analytics"),
        query={"charset": "utf8mb4"},
    )
    return create_engine(url, pool_pre_ping=True)

def validate_config():
    if not TOKEN or TOKEN.startswith("replace_"):
        raise RuntimeError("Add your TMDB token to your local .env file.")
