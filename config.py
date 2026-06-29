import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
DEVELOPER_ID = int(os.getenv('DEVELOPER_ID'))


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# har safar kerakli key yoki tokenlarni bir xil kod yozib bir nechta filelarda chaqirimasdan bitta configda yozib kerakli ma'lumotlarni imporrt qilib ishlatish uchun kerak 