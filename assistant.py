from openai import OpenAI

from aiogram.types import FSInputFile
import time
from config import TOKEN_API_ASSISTANT

client = OpenAI(api_key = TOKEN_API_ASSISTANT)

thread = client.beta.threads.create()

def text_to_voice(message, answer):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input= answer
    )

    speech_file_path = f"{message.from_user.id}.mp3"

    response.write_to_file(speech_file_path)
    audio = FSInputFile(speech_file_path, f"{message.from_user.id}.mp3")
    return audio

def get_answer(question):
    
    assistant = client.beta.assistants.create(
      name="VoiceAnswers",
      instructions="",
      model='gpt-4-1106-preview'
    )

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=question
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    while run.status != 'completed':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(run.status)
        time.sleep(1)
    print("Run completed!")

    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
    )

    answer = messages.data[0].content[0].text.value
    return answer

def voice_to_text(wav_file):
    audio_file = open(wav_file, "rb")
    question = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )
    return question