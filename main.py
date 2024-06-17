from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

import asyncio  
import ai_helper.ai_helper as AI
from config import TOKEN_API_BOT

from file_manager.file_manager import FileManager

TOKEN_API = TOKEN_API_BOT
bot = Bot(TOKEN_API)
dp = Dispatcher()

ai = AI.AI()

@dp.message(F.voice)
async def voice_message_handler(message:Message):

    if ai.permission is True:
        file_name = await FileManager.get_voice_file(bot, message)

        await message.answer("Голосовое сообщение получено!")
        question = await ai.voice_to_text(file_name)

        await message.answer("Получаю ответ...")
        answer, status = await ai.get_answer(question)
    
        if(status is False):
            message.reply(answer)

        else:
            await message.answer("Конвертирую в аудиофаил...")
            audio = await ai.text_to_voice(file_name, answer)
            await bot.send_voice(message.chat.id, audio, reply_to_message_id=message.message_id)

        FileManager.remove_files(file_name)
    
    else:
        error_answer = "К сожалению, использование чат-бота запрещено в вашем регионе :("
        await message.reply(error_answer)

@dp.message(Command("start"))
async def start_handler(message: Message):
    greeting = f'Привет, {message.from_user.full_name}! Я бот для получения аудио ответов!'
    instruction = 'Отправь мне голосовое сообщение с вопросом, а я найду ответ и озвучу его для тебя! Все просто ;)'

    await message.answer(greeting) 
    await message.answer(instruction)

@dp.message()
async def default_handler(message: Message):
    await message.answer("Я не знаю, что мне делать с этим :(")
    await message.answer("Отправь голосовое сообщение с вопросом, а я отвечу на него!")

async def main():
   await ai.init_assistant()
   await bot.delete_webhook(drop_pending_updates=True)
   await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
