import logging


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'INFO': '\033[94m',  # Blue for INFO
        'ERROR': '\033[91m', # Red for ERROR
        'RESET': '\033[0m',  # Reset color
    }

    def format(self, record):
        log_level = record.levelname
        color = self.COLORS.get(log_level, self.COLORS['RESET'])
        message = super().format(record)
        return f"{color}{message}{self.COLORS['RESET']}"


logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()

formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)