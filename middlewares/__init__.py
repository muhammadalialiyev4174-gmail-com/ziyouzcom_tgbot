from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
import time

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, slow_mode_delay=0.5):
        self.slow_mode_delay = slow_mode_delay
        self.users = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Check if event is a Message
        if not isinstance(event, Message):
            return await handler(event, data)
        
        user_id = event.from_user.id
        current_time = time.time()
        
        if user_id in self.users:
            if current_time - self.users[user_id] < self.slow_mode_delay:
                return # Ignore message if sent too fast
            
        self.users[user_id] = current_time
        return await handler(event, data)
