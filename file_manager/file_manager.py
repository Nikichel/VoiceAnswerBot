import os
from pydub import AudioSegment
import time
import base64


class FileManager:

    @classmethod
    # Удаление всех файлов, которые были созданы для ответа
    def remove_files(cls, file_name):
        mp3_file = f"{file_name}.mp3"
        ogg_file = mp3_file.replace('.mp3', '.ogg')
        wav_file = mp3_file.replace('.mp3', '.wav')

        if(os.path.exists(file_name)):
            os.remove(file_name)
        if os.path.exists(mp3_file):
            os.remove(mp3_file)
        if os.path.exists(ogg_file):
            os.remove(ogg_file)
        if os.path.exists(wav_file):
            os.remove(wav_file)

    @classmethod
    # Получение голосового сообщения и генерация названия файла
    async def get_voice_file(cls, bot, message):
        file_name = f'{message.from_user.id}_{time.time()}'
        ogg_file = f'{file_name}.ogg'
        wav_file = ogg_file.replace('.ogg', '.wav')

        file = await bot.get_file(message.voice.file_id)
        await bot.download_file(file.file_path, f'{ogg_file}')

        sound = AudioSegment.from_file(f'{ogg_file}') 
        sound.export(f'{wav_file}', format="wav")
        return file_name
    
    @classmethod
    # Получение голосового сообщения и генерация названия файла
    async def get_photo_file(cls, bot, message):
        file_name = f'{message.from_user.id}_{time.time()}'

        photo = message.photo[-1]

        photo_file = await bot.get_file(photo.file_id)
        await bot.download_file(photo_file.file_path, file_name)

        return file_name
    
    @classmethod
    async def encode_image(cls, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')