from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from urllib.parse import quote_plus
from core.common.loader.config_loader import ConfigLoader
from core.common.pattern.singleton import singleton


Base = declarative_base()


@singleton
class Settings:
    def __init__(self):
        self.db_cfg = ConfigLoader().config.database
        self.db_env = self.db_cfg.environment
        self.db_url = f"mysql+pymysql://root:%s@{self.db_cfg.host}:{self.db_cfg.port}/{self.db_env.MYSQL_DATABASE}" \
                 % quote_plus(self.db_env.MYSQL_ROOT_PASSWORD)

        self.engine = create_engine(
            url=self.db_url,
            pool_pre_ping=self.db_env.pool_pre_ping,
            pool_recycle=self.db_env.pool_recycle,
            pool_size=self.db_env.pool_size,
            max_overflow=self.db_env.max_overflow
        )

        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


def get_db() -> Generator:
    db = Settings().SessionLocal()
    try:
        yield db
    finally:
        db.close()
