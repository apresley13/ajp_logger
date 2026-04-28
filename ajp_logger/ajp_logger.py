"""
This is my attempt at a module with classes that can 
1. log to file with hourly rotation(ajp_logger_hourly)
2. log to file append without rotation(ajp_logger_tofile)

ap

"""
import sys
from datetime import datetime, timedelta

class ajp_logger_hourly:
    def __init__(self, log_dir="/Users/tasty/code/log/ajp_logger"):
        self.log_dir = log_dir
        self.console = sys.stdout
        self.file = None
        self.current_interval = None
        self._open_or_append_file()
    
    def _get_current_interval(self):
        now = datetime.now()
        hours = (now.hour // 1)
        return now.replace(hour=hours, minute=0, second=0, microsecond=0)
    
    def _get_log_filename(self, interval):
        return f"{self.log_dir}_{interval.strftime('%Y-%m-%d_%H-%M-%S')}.log"
    
    def _open_or_append_file(self):
        interval = self._get_current_interval()
        if self.current_interval != interval:
            if self.file:
                self.file.close()
            self.current_interval = interval
            filename = self._get_log_filename(interval)
            self.file = open(filename, 'a')
    
    def _check_rotation(self):
        self._open_or_append_file()
    
    def write(self, message):
        self._check_rotation()
        if message.strip():
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            message = f"[{timestamp}] {message}"
        
        self.file.write(message)
        self.file.flush()
    
    def flush(self):
        self.file.flush()
    
    def close(self):
        if self.file:
            self.file.close()

class ajp_logger_tofile:
    def __init__(self, log_file="/Users/tasty/code/log/ajp_logger.log"):
        self.log_file = log_file
        self.console = sys.stdout
        self.file = open(log_file, 'a')
    
    def write(self, message):
        if message.strip():
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            message = f"[{timestamp}] {message}"
        
        self.console.write(message)
        self.file.write(message)
        self.file.flush()
    
    def flush(self):
        self.console.flush()
        self.file.flush()
    
    def close(self):
        if self.file:
            self.file.close()