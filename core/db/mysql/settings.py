from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from urllib.parse import quote_plus
from core.common.loader.config_loader import ConfigLoader

db_cfg = ConfigLoader().database
db_env = db_cfg.environment
db_url = f"mysql+pymysql://root:%s@{db_cfg.host}:{db_cfg.port}/{db_env.MYSQL_DATABASE}" % quote_plus(db_env.MYSQL_ROOT_PASSWORD)

engine = create_engine(
    url=db_env.url,
    pool_pre_ping=db_env.pool_pre_ping,
    pool_recycle=db_env.pool_recycle,
    pool_size=db_env.pool_size,
    max_overflow=db_env.max_overflow
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
