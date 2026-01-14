import logging
from logging.handlers import RotatingFileHandler

LOG_FILE="logs/agent.log"

def setup_logger():
    logger=logging.getLogger("AI_AGENT")
    logger.setLevel(logging.DEBUG)

    ## to avoid duplicate logging, if log already exists use that one only
    if logger.handlers: 
        return logger
    
    #------------- CONSOLE Handler -----------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    console_formatter=logging.Formatter("%(levelname)s | %(message)s")
    console_handler.setFormatter(console_formatter)

    #------------- FILE Handler -----------
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )

    file_handler.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger