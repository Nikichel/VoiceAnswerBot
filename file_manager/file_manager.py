import os
from pydub import AudioSegment
import time

class FileManager:

    @staticmethod
    #Удаление всех файлов, которые были созданы для ответа
    def remove_files(file_name):
        mp3_file = f"{file_name}.mp3"
        ogg_file = mp3_file.replace('.mp3', '.ogg')
        wav_file = mp3_file.replace('.mp3', '.wav')

        if os.path.exists(mp3_file):
            os.remove(mp3_file)
        if os.path.exists(ogg_file):
            os.remove(ogg_file)
        if os.path.exists(wav_file):
            os.remove(wav_file)

    @staticmethod
    #Получение голосового сообщения и генерация названия файла
    async def get_voice_file(bot, message):
        file_name = f'{message.from_user.id}_{time.time()}'
        ogg_file = f'{file_name}.ogg'
        wav_file = ogg_file.replace('.ogg', '.wav')

        file = await bot.get_file(message.voice.file_id)
        await bot.download_file(file.file_path, f'{ogg_file}')

        sound = AudioSegment.from_file(f'{ogg_file}') 
        sound.export(f'{wav_file}', format="wav")
        return file_name