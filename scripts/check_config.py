from app.core.config import settings
from app.core.logger import logger

logger.info("App name: %s", settings.app_name)
logger.info("Database URL: %s", settings.database_url)