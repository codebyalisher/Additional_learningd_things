import logging
import os
from config.settings import settings
from logging.handlers import TimedRotatingFileHandler
from .mongo_logs import MongoHandler
from .log_cleaner import log_cleaner
from .sensitive_info import SecurityUtils


class SanitizingFormatter(logging.Formatter):
    """Formatter that sanitizes sensitive info before logging"""
    def format(self, record):
        msg = super().format(record)
        return SecurityUtils.sanitize_error_message(msg)

def setup_logging(mongo_uri=None, db_name=None, collection_name=None,
                 log_file=None, log_directory=None, log_level=None,
                 days_to_keep=None, cleanup_time=None, auto_cleanup=False):

    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Sanitizing formatter
    formatter = SanitizingFormatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = None
    try:
        if not os.path.exists(log_directory):
            os.makedirs(log_directory, exist_ok=True)

        log_file_path = os.path.join(log_directory, log_file)

        file_handler = TimedRotatingFileHandler(
            filename=log_file_path,
            when="midnight",
            interval=1,
            backupCount=0,
            encoding="utf-8",
            utc=True
        )
        file_handler.setLevel(getattr(logging, log_level))
        file_handler.setFormatter(formatter)
        file_handler.suffix = "%Y-%m-%d"

    except Exception as e:
        sanitized_error = SecurityUtils.sanitize_error_message(str(e))
        root_logger.error(f"Failed to setup file logging: {sanitized_error}")

    # Root logger
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.addHandler(console_handler)
    if file_handler:
        root_logger.addHandler(file_handler)

    # MongoDB handler
    if mongo_uri and db_name and collection_name:
        try:
            mongo_handler = MongoHandler(mongo_uri, db_name, collection_name)
            mongo_handler.setLevel(getattr(logging, log_level))
            mongo_handler.setFormatter(formatter)
            root_logger.addHandler(mongo_handler)
            root_logger.info("MongoDB logging enabled successfully")
        except Exception as e:
            sanitized_error = SecurityUtils.sanitize_error_message(str(e), [mongo_uri])
            root_logger.error(f"Failed to setup MongoDB logging: {sanitized_error}")
    else:
        root_logger.info("MongoDB logging disabled - missing configuration")

    # Log cleaner
    try:
        log_cleaner.log_directory = log_directory
        log_cleaner.log_base_name = log_file
        log_cleaner.days_to_keep = days_to_keep
        log_cleaner.cleanup_time = cleanup_time
        log_cleaner.auto_cleanup = auto_cleanup

        if auto_cleanup:
            log_cleaner.start_scheduled_cleanup()

        log_cleaner.cleanup_old_logs()
    except Exception as e:
        sanitized_error = SecurityUtils.sanitize_error_message(str(e))
        root_logger.error(f"Failed to setup log cleaner: {sanitized_error}")

    root_logger.info("Logging setup completed successfully")
    return root_logger


def log_with_context(logger, level, message, **context):
    """Log with sanitized extra context"""
    try:
        sanitized_context = SecurityUtils.sanitize_dict(context)
        if level == "info":
            logger.info(message, extra=sanitized_context)
        elif level == "warning":
            logger.warning(message, extra=sanitized_context)
        elif level == "error":
            logger.error(message, extra=sanitized_context)
        elif level == "debug":
            logger.debug(message, extra=sanitized_context)
        elif level == "critical":
            logger.critical(message, extra=sanitized_context)
    except Exception as e:
        getattr(logger, level)(f"{message} [Context logging failed: {e}]")
