import logging
import sys
import os
from datetime import datetime

# ANSI color codes for log levels
COLORS = {
    "DEBUG": "\033[36m",    # Cyan
    "INFO": "\033[32m",     # Green
    "WARNING": "\033[33m",  # Yellow
    "ERROR": "\033[31m",    # Red
    "RESET": "\033[0m",
}

class ColorFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, use_color=True):
        super().__init__(fmt, datefmt)
        self.use_color = use_color

    def format(self, record):
        msg = super().format(record)
        if self.use_color and record.levelname in COLORS:
            color = COLORS[record.levelname]
            reset = COLORS["RESET"]
            msg = f"{color}{msg}{reset}"
        return msg

class Log:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def __init__(self, level="basic", log_file=None, use_color=True):
        if Log._initialized:
            return
        self.level = level
        self.use_color = use_color
        self.logger = logging.getLogger("note_interpreter")
        self.logger.setLevel(logging.DEBUG if level == "debug" else logging.INFO)
        self.logger.handlers = []
        fmt = '%(asctime)s %(levelname)s %(message)s'
        # Console handler (with color)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColorFormatter(fmt, use_color=use_color))
        self.logger.addHandler(console_handler)
        # File handler (no color)
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
    def print(self, msg):
        print(msg)

    def reset(self):
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        Log._initialized = False
        Log._instance = None

# Singleton instance for easy import
log = Log() 