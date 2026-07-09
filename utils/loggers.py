import logging
import os
from logging.handlers import RotatingFileHandler
# barcha xatoliklar bo'layotgan actionlarni note ya'ni o'zida saqlab boradi
os.makedirs('logs', exist_ok=True) 

def setup_logger(name: str ='bot') ->logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H-%m-%s",
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    
    file_handler = RotatingFileHandler(
        filename='logs/bot.log',
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding='utf-8' 
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    error_handler = RotatingFileHandler(
        filename='logs/errors.log',
        maxBytes=2*1024*1024,
        backupCount=2,
        encoding='utf-8'    
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    
    return logger

logger = setup_logger()
# sql da yoziladigan commandalar dasturlash tilida yozilsa ORM deyiladi 