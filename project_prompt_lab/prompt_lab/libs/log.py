import logging
import sys
import os
from datetime import datetime

class Log:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def __init__(self, level="basic", log_file=None, use_color=True, to_console=False):
        if Log._initialized:
            return
        self.level = level
        self.logger = logging.getLogger("note_interpreter")
        self.logger.setLevel(logging.DEBUG if level == "debug" else logging.INFO)
        self.logger.handlers = []
        fmt = '%(asctime)s %(levelname)s %(message)s'
        # Console handler csak ha to_console True!
        if to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(fmt))
            self.logger.addHandler(console_handler)
        # File handler
        if level == "debug":
            if not log_file:
                log_dir = "logs"
                os.makedirs(log_dir, exist_ok=True)
                log_file = os.path.join(log_dir, f"llm_agent_debug_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
            file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(fmt))
            self.logger.addHandler(file_handler)
        Log._initialized = True

    def debug(self, msg):
        self.logger.debug(msg)
    def info(self, msg):
        self.logger.info(msg)
    def warning(self, msg):
        self.logger.warning(msg)
    def error(self, msg):
        self.logger.error(msg)

    def reset(self):
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        Log._initialized = False
        Log._instance = None

# Singleton instance for easy import
log = Log() 