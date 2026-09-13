from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.database_models import Base


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "enterprise.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def create_tables() -> None:
    """Create all database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a database session and close it safely."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()