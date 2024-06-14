from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

import asyncio  
import assistant
from config import TOKEN_API_BOT

import functions

TOKEN_API = TOKEN_API_BOT
bot = Bot(TOKEN_API)
dp = Dispatcher()  

@dp.message(F.voice)
async def a(message:Message):
        
    wav_file = await functions.get_voice_file(bot, message) 

    await message.answer("Голосовое сообщение получено!")
    question = assistant.voice_to_text(wav_file)

    await message.answer("Получаю ответ...")
    answer = assistant.get_answer(question)

    await message.answer("Конвертирую в аудиофаил...")
    audio = assistant.text_to_voice(message, answer)

    await bot.send_audio(message.chat.id, audio, title=f"Ответ для {message.from_user.first_name}")

    functions.remove_files(message)

@dp.message(Command("start"))
async def start(message: Message):
    greeting = f'Привет, {message.from_user.full_name}! Я бот для получения аудио ответов!'
    instruction = 'Отправь мне голосовое сообщение с вопросом, а я найду ответ и озвучу его для тебя! Все просто ;)'

    await message.answer(greeting) 
    await message.answer(instruction) 


async def main():
   await bot.delete_webhook(drop_pending_updates=True)
   await dp.start_polling(bot) 

if __name__ == '__main__':
    asyncio.run(main())