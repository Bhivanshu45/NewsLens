from sqlalchemy import text

from app.core.logger import logger
from app.db.session import engine


with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))

    logger.info("Database check result: %s", result.scalar())