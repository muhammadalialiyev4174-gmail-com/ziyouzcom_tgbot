import logging
from aiogram.exceptions import (
    TelegramUnauthorizedError, TelegramAPIError, TelegramRetryAfter,
    TelegramBadRequest
)
from aiogram.types import ErrorEvent

from loader import dp

@dp.error()
async def errors_handler(event: ErrorEvent):
    """
    Exceptions handler. Catches all exceptions.
    """
    exception = event.exception

    if isinstance(exception, TelegramUnauthorizedError):
        logging.exception(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, TelegramRetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {event.update}')
        return True

    if isinstance(exception, TelegramBadRequest):
        logging.exception(f'BadRequest: {exception} \nUpdate: {event.update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {event.update}')
        return True
        
    logging.exception(f'Update: {event.update} \n{exception}')
