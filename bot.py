import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from config import SPAM_KEYWORDS, is_spam

logging.basicConfig(level=logging.INFO)

TOKEN = "7938100044:AAEkskIwInsETF6v5dSXyZJ6OV1aZNen9ng"
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)

def replace_hidden_chars(text):
    replacements = {
        'C': 'С', 'H': 'Н', 'O': 'О',
        'u': 'и', '3': 'з', '6': 'б',
        'Y': 'У', 'd': 'д', 'e': 'е',
        'n': 'н', 'c': 'с', 'p': 'р',
        'a': 'а', 'b': 'в', 'o': 'о',
        't': 'т', 'k': 'к', 'm': 'м',
        'x': 'х', 'r': 'р', 'q': 'к',
        's': 'с', 'l': 'л', 'j': 'й',
        'v': 'в', 'i': 'и', 'g': 'г',
        'T': 'Т', 'A': 'А', 'B': 'Б',
        'E': 'Е', 'K': 'К', 'M': 'М',
        'X': 'Х', 'Z': 'З', '4': 'ч', 'α': 'а', 'ρ':'р', 'U':'и'
    }

    for latin_char, russian_char in replacements.items():
        text = text.replace(latin_char, russian_char)

    text = text.replace(' ', '')

    return text

@router.message(F.text == "chat_id")
async def handle_chat_id(message: Message):
    chat_id = message.chat.id
    await message.reply(f"ID этого чата: {chat_id}")

@dp.message(F.text)
async def handle_message(message: Message):
    message_text = replace_hidden_chars(message.text)
    if any(keyword in message.text.lower() for keyword in SPAM_KEYWORDS) or is_spam(message.text.lower()) or any(keyword in message_text.lower() for keyword in SPAM_KEYWORDS):
        try:
            # Попытка отправить сообщение в первый чат
            await bot.send_message(471761840, f"Delete message:\n\n {message.text}")
        except Exception as e:
            logging.warning(f"Не удалось отправить сообщение в чат 471761840: {e}")

        try:
            # Попытка отправить сообщение во второй чат
            await bot.send_message(356780793, f"Delete message:\n\n {message.text}")
        except Exception as e:
            logging.warning(f"Не удалось отправить сообщение в чат 356780793: {e}")

        try:
            # Удаление сообщения
            await message.delete()
            logging.info(f'Message deleted: {message.text}')

            # Блокировка пользователя
            await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
            logging.info(f'User {message.from_user.id} banned.')

        except Exception as e:
            logging.error(f"Ошибка при удалении сообщения или блокировке пользователя: {e}")

    if len(message.text) > 1000:
        try:
            await message.delete()
        except Exception as e:
            logging.error(f"Ошибка при удалении длинного сообщения: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
