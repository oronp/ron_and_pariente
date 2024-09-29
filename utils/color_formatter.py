import logging

# ANSI escape sequences for colors
RESET = "\033[0m"
COLORS = {
    'DEBUG': "\033[94m",  # Blue
    'INFO': "\033[98m",  # Grey
    'WARNING': "\033[93m",  # Yellow
    'ERROR': "\033[91m",  # Red
    'CRITICAL': "\033[95m"  # Magenta
}


class ColorFormatter(logging.Formatter):
    """Custom formatter to add colors based on log levels."""

    def format(self, record):
        log_color = COLORS.get(record.levelname, RESET)  # Get color based on log level
        message = super().format(record)  # Format the original message
        return f"{log_color}{message}{RESET}"  # Return colored message
