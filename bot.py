import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from config import SPAM_KEYWORDS, is_spam

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
TOKEN = "7938100044:AAEkskIwInsETF6v5dSXyZJ6OV1aZNen9ng"
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)

@router.message(F.text == "chat_id")
async def handle_chat_id(message: Message):
    chat_id = message.chat.id
    await message.reply(f"ID этого чата: {chat_id}")

# Проверка сообщений на наличие спам-ключевых слов
@dp.message(F.text)
async def handle_message(message: Message):
    if any(keyword in message.text.lower() for keyword in SPAM_KEYWORDS) or is_spam(message.text.lower()):
        try:
            # Удаление сообщения
            await message.delete()

            logging.info(f'Message: {message.text}')
            
            # Блокировка пользователя
            await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
            
        except Exception as e:
            logging.error(f"Ошибка при удалении сообщения или блокировке пользователя: {e}")

    if len(message.text) > 1000:
        try:
            await message.delete()
        except Exception as e:
            logging.error(f"Ошибка при удалении сообщения или блокировке пользователя: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
