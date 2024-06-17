from openai import AsyncOpenAI
from aiogram.types import FSInputFile
from config import TOKEN_API_ASSISTANT

#Класс для работы с OpenAI
class AI:
    def __init__ (self):
        self.client = AsyncOpenAI(api_key=TOKEN_API_ASSISTANT)
        self.assistant = None

    #Преобразование текста в звук (OpenAI TTS API)
    async def text_to_voice(self, file_name, answer):
        response = await self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=answer
        )

        speech_file_path = f"{file_name}.mp3"

        response.write_to_file(speech_file_path)
        audio = FSInputFile(speech_file_path)
        return audio

    #Получение ответа из голосового сообщения (OpenAI Assistant API)
    async def get_answer(self, question):

        if (self.assistant is None):
            self.assistant = await self.client.beta.assistants.create(
                name="VoiceAnswers",
                instructions="",
                model='gpt-4-1106-preview'
            )
        
        thread = await self.client.beta.threads.create()

        await self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role='user',
            content=question
        )

        run = await self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, 
            assistant_id=self.assistant.id
        )

        if run.status in ['completed', 'requires_action', 'failed']:
            if run.status == 'completed':
                messages = await self.client.beta.threads.messages.list(thread_id=thread.id)
                answer = messages.data[0].content[0].text.value
                return answer, True
            elif run.status == 'requires_action':
                return "Задача требует дальнейших действий.", False
            elif run.status == 'failed':
                return "Задача не была выполнена.", False
        else:
            return "Задача все еще выполняется или имеет неизвестный статус.", False

        messages = await self.client.beta.threads.messages.list(
            thread_id=thread.id,
        )

    #Конвертация голоса в текст (Whisper OpenAI API)
    async def voice_to_text(self, file_name):
        audio_file = open(f"{file_name}.wav", "rb")
        question = await self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )
        audio_file.close()
        return question