import os
import glob
import time
import schedule
import threading
import logging

class LogCleaner:
    def __init__(self):
        self.log_directory = "logs"
        self.log_base_name = "app.log"
        self.days_to_keep = 7
        self.cleanup_time = "02:00"
        self.auto_cleanup = False
        self.running = False
        self.logger = logging.getLogger(__name__)
        
    def cleanup_old_logs(self):
        """Clean up log files older than specified days"""
        if self.days_to_keep <= 0:
            return
            
        current_time = time.time()
        cutoff_time = current_time - (self.days_to_keep * 24 * 3600)
        
        # Ensure log directory exists
        if not os.path.exists(self.log_directory):
            self.logger.warning(f"Log directory {self.log_directory} does not exist")
            return
            
        # Pattern for rotated log files
        patterns = [
            f"{self.log_base_name}.*",
            f"{self.log_base_name}-*",
        ]
        
        deleted_count = 0
        for pattern in patterns:
            files = glob.glob(os.path.join(self.log_directory, pattern))
            for file_path in files:
                try:
                    if (os.path.isfile(file_path) and 
                        os.path.getmtime(file_path) < cutoff_time):
                        os.remove(file_path)
                        deleted_count += 1
                        self.logger.info(f"Deleted old log file: {os.path.basename(file_path)}")
                except (OSError, Exception) as e:
                    self.logger.error(f"Error deleting log file {file_path}: {e}")
        
        if deleted_count > 0:
            self.logger.info(f"Cleaned up {deleted_count} old log files (retention: {self.days_to_keep} days)")
    
    def start_scheduled_cleanup(self):
        """Start scheduled cleanup if enabled"""
        if self.auto_cleanup:
            self.running = True
            
            # Schedule daily cleanup
            schedule.every().day.at(self.cleanup_time).do(self.cleanup_old_logs)
            
            def run_scheduler():
                while self.running:
                    schedule.run_pending()
                    time.sleep(60)  # Check every minute
                    
            # Start scheduler in background thread
            self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            self.scheduler_thread.start()
            self.logger.info(f"Log cleanup scheduler started (runs daily at {self.cleanup_time})")
        else:
            self.logger.info("Auto log cleanup is disabled")
    
    def stop_scheduled_cleanup(self):
        """Stop the scheduled cleanup"""
        self.running = False
        if hasattr(self, 'scheduler_thread'):
            self.scheduler_thread.join(timeout=1.0)

# Singleton instance
log_cleaner = LogCleaner()