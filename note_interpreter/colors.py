# ANSI színkódok kizárólag user-facing outputhoz (user_print)
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
GREEN = "\033[32m"
RED = "\033[31m"
WHITE = "\033[37m"

BANNER_COLORS = {
    "SYSTEM PROMPT": CYAN,
    "LLM RESPONSE": YELLOW,
    "TOOL CALL": MAGENTA,
    "FINAL OUTPUT": GREEN,
    "FINAL OUTPUT (FALLBACK)": RED,
} 