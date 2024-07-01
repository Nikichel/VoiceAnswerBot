import threading

from amplitude.client import Amplitude, BaseEvent
from concurrent.futures import ThreadPoolExecutor

from config import TOKEN_AMPLITUDE

amplitude = Amplitude(TOKEN_AMPLITUDE)

class ObserverEvent(object):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls, *args, **kwargs)
                cls._instance.executor = ThreadPoolExecutor(max_workers=5)
        return cls._instance
    
    def send_event_to_amplitude(cls, event_type, user_id):  
        event = BaseEvent(
                event_type=event_type,
                user_id=str(user_id)
            )
        
        amplitude.track(event)
        print(f"{event_type}: {user_id} send")

    def track_event(cls, event_name, user_id):
        cls._instance.executor.submit(cls.send_event_to_amplitude(event_name, user_id))
        