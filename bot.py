"""
This is a bot.
"""
import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    chat_id = message.chat.id
    await message.reply(f"Бот для контроля отправления\nпрогнозов заказчику.\nДля включения в рассылку напишите\nсвой chat id в ЛС @senchilo_nikita.\nChat id = {chat_id}")
    
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)