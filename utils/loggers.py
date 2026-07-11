import logging
import os
from logging.handlers import RotatingFileHandler
# barcha xatoliklar bo'layotgan actionlarni note ya'ni o'zida saqlab boradi
os.makedirs('logs', exist_ok=True)  # bu yerda folder ya'ni papka yaratgan loyihani ichida 
 
def setup_logger(name: str ='bot') ->logging.Logger: # bu joyida esa setup qilishni boshlagan ya'ni qnaday qilib loglarni o'zimizga o'qishga moslab chiroyli qilib olish uchun 

    logger = logging.getLogger(name) # bu joyda logni olgin hamda meng akerakli nomini ber ya'ni logni nomi nimaligini 
    logger.setLevel(logging.DEBUG) # bu yerda DEBUG  levelidagi loglarni chiqar ya'ni hech qanday xatoligi mavjud bo'lmagan to'g'ri ma'lumotlarni
    
    formatter = logging.Formatter( # bu bilan formatlaganmz, ya'ni  bizga kerakli bo'lgan loglarni qnaday formatda qabul qilishni so'raganmiz
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", # bu yerda logni async bo'lgan vaqti , qanaqa leveldagi log logni nomi hamda unda qaytayotgan message
        datefmt="%Y-%m-%d %H-%m-%s", # bu yerda yil oy kun soat minut sekund larni olishini so'raganmiz 
    )
    
    console_handler = logging.StreamHandler() # bu yerda ularni consolega chiqarish ya'ni terminalga chiqarishini aytganmiz handlarni
    console_handler.setLevel(logging.DEBUG)# bu yerda esa debuglar console ga chiqishi aytilgan
    console_handler.setFormatter(formatter) # formatlangan ma'lumotlarlar terminalga chiqishi aytilgan 
    
    file_handler = RotatingFileHandler( # endi uni file ko'rinishi olish 
        filename='logs/bot.log', # logni ichidagi bot.log degan file yaratishini aytganmiz
        maxBytes=5*1024*1024,  # hamma computerlar internet haqida gap ketsa ular eng kichigidan bohslab hisoblayti ya'ni Byte 'larda , byte bu megabyte ni ildiz ostisi ya'ni byteni kvadratga oshirsak megabyte bo'ladi bu yerda biz file 5 mb gacha bo'lsin deganmiz
        backupCount=3, 
        encoding='utf-8' 
    )
    file_handler.setLevel(logging.DEBUG) # fileni qanaqa turda saqlashi aytilgan 
    file_handler.setFormatter(formatter) # o'sha file ichidagi ma'lumot albatta formatlangan bo'lishi kerak 
    
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