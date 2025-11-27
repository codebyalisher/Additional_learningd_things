import logging
import os
import glob
import time
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta

class TimedRotatingFileHandlerWithDeletion(TimedRotatingFileHandler):
    def __init__(self, filename, when='midnight', interval=1, backupCount=0, 
                 encoding=None, delay=False, utc=False, atTime=None,
                 delete_after_days=7):
        super().__init__(filename, when, interval, backupCount, 
                        encoding, delay, utc, atTime)
        self.delete_after_days = delete_after_days
        self._delete_old_logs()
    
    def _delete_old_logs(self):
        """Delete log files older than delete_after_days"""
        if self.delete_after_days <= 0:
            return
            
        current_time = time.time()
        cutoff_time = current_time - (self.delete_after_days * 24 * 3600)
        
        # Get all log files matching the pattern
        log_dir = os.path.dirname(self.baseFilename) or '.'
        log_base = os.path.basename(self.baseFilename)
        
        # Pattern for rotated files
        patterns = [
            f"{log_base}.*",
            f"{log_base}.*.*",
        ]
        
        for pattern in patterns:
            files = glob.glob(os.path.join(log_dir, pattern))
            for file_path in files:
                try:
                    if (os.path.isfile(file_path) and 
                        os.path.getmtime(file_path) < cutoff_time and 
                        os.path.abspath(file_path) != os.path.abspath(self.baseFilename)):
                        os.remove(file_path)
                        print(f"Deleted old log file: {file_path}")
                except (OSError, Exception) as e:
                    print(f"Error deleting log file {file_path}: {e}")
    
    def doRollover(self):
        """Override doRollover to include deletion of old files"""
        super().doRollover()
        self._delete_old_logs()