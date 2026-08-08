import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import declarative_base, sessionmaker


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SSL_CA = os.getenv("DB_SSL_CA")


# =========================================================
# VALIDATE REQUIRED VARIABLES
# =========================================================

required_variables = {
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_SSL_CA": DB_SSL_CA,
}


missing_variables = [
    name
    for name, value in required_variables.items()
    if not value
]


if missing_variables:
    raise RuntimeError(
        "Missing required database environment variables: "
        + ", ".join(missing_variables)
    )


# =========================================================
# SSL CERTIFICATE PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

SSL_CA_PATH = BASE_DIR / DB_SSL_CA


if not SSL_CA_PATH.exists():
    raise RuntimeError(
        f"MySQL CA certificate was not found at: {SSL_CA_PATH}"
    )


# =========================================================
# DATABASE URL
# =========================================================

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)


# =========================================================
# DATABASE ENGINE
# =========================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": str(SSL_CA_PATH),
        }
    },
    pool_pre_ping=True,
)


# =========================================================
# SESSION
# =========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# =========================================================
# BASE MODEL
# =========================================================

Base = declarative_base()


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()