
from redis.asyncio import Redis
from config import REDIS_HOST, REDIS_PORT
from aiogram.fsm.storage.redis  import RedisStorage 

# Создание подключения к Redis
#redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# Инициализация хранилища состояний для aiogram
#storage = RedisStorage(redis)