import logging
logger = logging.getLogger("uvicorn.error")

logger.info("Application started")

# Setup logging with safe fallback
def safe_setup_logging():
    try:
        logger = setup_logging(
            mongo_uri=settings.MONGO_URI,
            db_name=settings.MONOG_DB_NAME,
            collection_name=settings.MONGO_LOG_COLLECTION,
            log_file=settings.LOG_FILE,
            log_directory=settings.LOG_DIRECTORY,
            log_level=settings.LOG_LEVEL,
            days_to_keep=settings.LOG_RETENTION_DAYS,
            cleanup_time=settings.LOG_CLEANUP_TIME,
            auto_cleanup=settings.LOG_AUTO_CLEANUP
        )
        return logger
        
    except Exception as e:
        print(f"Advanced logging setup failed: {e}. Falling back to basic file logging...")
        
        # Fallback to basic file logging without MongoDB
        try:
            # Create log directory if it doesn't exist
            import os
            log_dir = getattr(settings, 'LOG_DIRECTORY', 'logs')
            log_file = getattr(settings, 'LOG_FILE', 'app.log')
            
            if not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            log_path = os.path.join(log_dir, log_file)
            
            # Basic file logging
            logging.basicConfig(
                level=getattr(logging, getattr(settings, 'LOG_LEVEL', 'INFO')),
                format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                handlers=[
                    logging.FileHandler(log_path, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )
            print(f"Basic file logging enabled: {log_path}")
            
        except Exception as file_error:
            print(f"File logging also failed: {file_error}. Using console logging only.")
            logging.basicConfig(level=logging.INFO)
        
        return logging.getLogger(__name__)

# Use safe setup
logger = safe_setup_logging()

# Test logging immediately
logger.info("Application starting up...")
logger.info(f"Log directory: {getattr(settings, 'LOG_DIRECTORY', 'logs')}")
logger.info(f"Log file: {getattr(settings, 'LOG_FILE', 'app.log')}")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
