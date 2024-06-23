from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from Reflex_fastapi_with_admin.configs.config import ENGINE_URI
from Reflex_fastapi_with_admin.utils.LoggerSingleton import logger

engine = create_engine(ENGINE_URI, connect_args={"check_same_thread": False}, echo=True)
Base = declarative_base()
logger.info("Engine created")




