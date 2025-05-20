from note_interpreter.colors import RESET, BOLD, CYAN, YELLOW, MAGENTA, BLUE, GREEN, RED, WHITE

def user_print(message, color=WHITE, bold=False):
    prefix = ""
    if bold:
        prefix += BOLD
    print(f"{prefix}{color}{message}{RESET}")

# Szín shortcutok exportálása
__all__ = [
    "user_print", "RESET", "BOLD", "CYAN", "YELLOW", "MAGENTA", "BLUE", "GREEN", "RED", "WHITE"
] 