import os
from pydub import AudioSegment

def remove_files(message):
    mp3_file = f"{message.from_user.id}.mp3"
    ogg_file = mp3_file.replace('.mp3', '.ogg')
    wav_file = mp3_file.replace('.mp3', '.wav')

    if os.path.exists(mp3_file):
        os.remove(mp3_file)
    if os.path.exists(ogg_file):
        os.remove(ogg_file)
    if os.path.exists(wav_file):
        os.remove(wav_file)

async def get_voice_file(bot, message):
    ogg_file = f'{message.from_user.id}.ogg'
    wav_file = ogg_file.replace('.ogg', '.wav')

    file = await bot.get_file(message.voice.file_id)
    await bot.download_file(file.file_path, f'{ogg_file}')

    sound = AudioSegment.from_file(f'{ogg_file}') 
    sound.export(f'{wav_file}', format="wav")
    return wav_file