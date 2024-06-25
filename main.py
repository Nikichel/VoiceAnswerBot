from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import asyncio  
import ai_helper.ai_helper as AI
from config import TOKEN_API_BOT, ID_ASSISTANT

from file_manager.file_manager import FileManager

from amplitude_client.amplitude_client import ObserverEvent

from database.redis import storage

TOKEN_API = TOKEN_API_BOT
bot = Bot(TOKEN_API)
dp = Dispatcher(storage = storage)

ai = AI.AI()
observer = ObserverEvent()

@dp.message(F.voice)
async def voice_message_handler(message:Message, state: FSMContext):

    if ai.permission is True:
        file_name = await FileManager.get_voice_file(bot, message)

        await message.answer("Голосовое сообщение получено!")
        question = await ai.voice_to_text(file_name)

        await message.answer("Получаю ответ...")
        answer, status = await ai.get_answer(question, message.from_user.id, state, message.chat.id)
    
        if(status is False):
            message.reply(answer)

        else:
            await message.answer("Конвертирую в аудиофаил...")
            audio = await ai.text_to_voice(file_name, answer)
            await bot.send_voice(message.chat.id, audio, reply_to_message_id=message.message_id)
        
        observer.send_event_to_amplitude("voise_question", message.from_user.id)
        FileManager.remove_files(file_name)
    
    else:
        error_answer = "К сожалению, использование чат-бота запрещено в вашем регионе :("
        await message.reply(error_answer)

@dp.message(F.photo)
async def photo_message_handler(message: Message):

    file_name_photo = await FileManager.get_photo_file(bot, message)

    emotions = await ai.image_to_mood(file_name_photo)

    audio = await ai.text_to_voice(file_name_photo, emotions)

    await bot.send_voice(message.chat.id, audio, reply_to_message_id=message.message_id)

    observer.send_event_to_amplitude("photo_emotion", message.from_user.id)
    FileManager.remove_files(file_name_photo)


@dp.message(Command("start"))
async def start_handler(message: Message):
    greeting = f'Привет, {message.from_user.full_name}! Я бот для получения аудио ответов!'
    instruction = 'Отправь мне голосовое сообщение с вопросом, а я найду ответ и озвучу его для тебя! Все просто ;)'

    observer.send_event_to_amplitude("user_start", message.from_user.id)
    await message.answer(greeting) 
    await message.answer(instruction)

@dp.message()
async def default_handler(message: Message):
    observer.send_event_to_amplitude("unknown_command", message.from_user.id)
    await message.answer("Я не знаю, что мне делать с этим :(")
    await message.answer("Отправь голосовое сообщение с вопросом, а я отвечу на него!")

async def main():
   await ai.init_assistant(ID_ASSISTANT)
   await ai.update_assistant()
   await bot.delete_webhook(drop_pending_updates=True)
   await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
