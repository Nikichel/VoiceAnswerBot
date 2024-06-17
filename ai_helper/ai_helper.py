import openai
from aiogram.types import FSInputFile
from config import TOKEN_API_ASSISTANT

#Класс для работы с OpenAI
class AI:

    __client = openai.AsyncOpenAI(api_key=TOKEN_API_ASSISTANT)
    __assistant = None

    async def init_assistant(self):
        if(self.__assistant == None):
            try:
                self.__assistant = await self.__client.beta.assistants.create(
                    name="VoiceAnswers",
                    instructions="",
                    model='gpt-4-1106-preview'
                )
                self.permission = True
            except openai.PermissionDeniedError:
                self.permission = False

    #Преобразование текста в звук (OpenAI TTS API)
    async def text_to_voice(self, file_name, answer):
        response = await AI.__client.audio.speech.create(
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
        
        thread = await AI.__client.beta.threads.create()

        await AI.__client.beta.threads.messages.create(
            thread_id=thread.id,
            role='user',
            content=question
        )

        run = await AI.__client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, 
            assistant_id=self.__assistant.id
        )

        if run.status in ['completed', 'requires_action', 'failed']:
            if run.status == 'completed':
                messages = await AI.__client.beta.threads.messages.list(thread_id=thread.id)
                answer = messages.data[0].content[0].text.value
                return answer, True
            elif run.status == 'requires_action':
                return "Задача требует дальнейших действий.", False
            elif run.status == 'failed':
                return "Задача не была выполнена.", False
        else:
            return "Задача все еще выполняется или имеет неизвестный статус.", False

        messages = await AI.__client.beta.threads.messages.list(
            thread_id=thread.id,
        )

    #Конвертация голоса в текст (Whisper OpenAI API)
    async def voice_to_text(self, file_name):
        audio_file = open(f"{file_name}.wav", "rb")
        question = await AI.__client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )
        audio_file.close()
        return question