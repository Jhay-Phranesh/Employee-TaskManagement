import os
import logging
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
os.makedirs("app/logs", exist_ok=True)

logger = logging.getLogger("employee_task_manager")

logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "app/logs/app.log",
    maxBytes=1024 * 1024,
    backupCount=3
)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

handler.setFormatter(formatter)

logger.addHandler(handler)