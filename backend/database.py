import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/product_db",
)

# Detectar si es SQLite para configurar opciones apropiadas
is_sqlite = DATABASE_URL.startswith("sqlite")

if is_sqlite:
    # SQLite: sin pool options (no son compatibles)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if ":///:" not in DATABASE_URL else {}
    )
else:
    # PostgreSQL: con pool options
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
        max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
