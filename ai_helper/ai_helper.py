import openai
from aiogram.types import FSInputFile
from config import TOKEN_API_CLIENT
from ai_helper.ai_tools import valid_tools, assistant_tools
import json

from database.database import DataBaseHelper
#Класс для работы с OpenAI
class AI:

    __client = openai.AsyncOpenAI(api_key=TOKEN_API_CLIENT)
    __assistant = None
    __db = DataBaseHelper()

    async def init_assistant(self, assistant_id = None):
        try:
            if(assistant_id is not None):
                    self.__assistant = await self.__client.beta.assistants.retrieve(assistant_id=assistant_id)
                    self.permission = True
            if(self.__assistant is None):
                self.__assistant = await self.__client.beta.assistants.create(
                    name="VoiceAnswers",
                    instructions="""
                            You are the Russian chat assistant. You can answer questions and participate in the conversation. 
                            Analyze the user messages and try to identify the user's key values based on your
                            communication. If any values are found, then call the save_value function. Don't forget 
                            to continue your ordinary dialogue with the user after you call save_value function.
                        """,
                    model='gpt-4',
                    tools= assistant_tools
                )
                print(self.__assistant.id)
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
    async def get_answer(self, question, user_id):
        
        thread = await AI.__client.beta.threads.create()

        await AI.__client.beta.threads.messages.create(
            thread_id=thread.id,
            role='user',
            content=question
        )

        run = await AI.__client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, 
            assistant_id=self.__assistant.id,
            tool_choice="required"
        )

        while run.status in ['completed', 'requires_action', 'failed']:
            
            print(run.status)
            if run.status == 'requires_action':
                run, userid_and_values = await self.get_values(user_id, thread, run)
                await self.validate_values(userid_and_values, question)
            
            elif run.status == 'failed':
                return "Задача не была выполнена.", False
            
            elif run.status == 'completed':
                messages = await AI.__client.beta.threads.messages.list(thread_id=thread.id)
                answer = messages.data[0].content[0].text.value
                
                print(userid_and_values)
                return answer, True 
        return "Задача все еще выполняется или имеет неизвестный статус.", False

    async def get_values(self, user_id, thread, run):
        tool_outputs = []
        userid_and_values = []
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            print(tool.function.arguments)
            value_dict = json.loads(tool.function.arguments)
            values = value_dict.get('values', [])

            tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": tool.function.arguments
                    })
                    
            userid_and_values.append({
                        "values": values,
                        "user_id": user_id
                    })
        if tool_outputs:
            try:
                run = await AI.__client.beta.threads.runs.submit_tool_outputs_and_poll(
                            thread_id=thread.id,
                            run_id=run.id,
                            tool_outputs=tool_outputs
                        )
            except Exception as e:
                print(f"Failed to submit tool outputs: {e}")
        return run, userid_and_values
    
    async def validate_values(self, userid_and_values, question):
        for item in userid_and_values:
            for value in item['values']:
                is_valid = await self.is_life_value(value, question)
                if is_valid:
                    print(f"User ID: {item['user_id']}, Value: {value}")
                    await self.__db.insert_data(user_id=item['user_id'], value=value)
                else:
                    print(f"Value '{value}' is not a key life value for user ID {item['user_id']}")

    async def is_life_value(self, value: str, question: str) -> bool:
        messages=[
            {"role": "user", "content": f"Is \"{value}\" a key life value for question \"{question}\"? Answer only true or false."}
        ]
        
        try:
            response = await AI.__client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                tools=valid_tools,
                tool_choice="required"
            )
            tool_calls = response.choices[0].message.tool_calls
            if tool_calls:
                for tool_call in tool_calls:
                    if tool_call.function:
                        function_arguments = json.loads(tool_call.function.arguments)
                        print(function_arguments)
                        is_value = function_arguments['is_value']
                        print(is_value)
            return is_value
        except Exception as e:
            print(f"Error while checking if '{value}' is a key life value: {e}")
            return False

    #Конвертация голоса в текст (Whisper OpenAI API)
    async def voice_to_text(self, file_name):
        with open(f"{file_name}.wav", "rb") as audio_file:
            question = await AI.__client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file, 
                response_format="text"
            )
        return question