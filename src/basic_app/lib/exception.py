"""Define common error response format."""
from typing import (
    List,
    Any,
)
from enum import Enum
import fastapi
from fastapi import responses
from fastapi.exceptions import RequestValidationError

class ErrorCode(Enum):
    """Define generic error code for this app."""
    INVALID_INPUT = (400, "Request validation error.")
    AUTHENTICATION_FAIL = (401, "Failed to authentiacate user.")
    EMAIL_ALEADY_EXISTS = (409, "This email is already registered.")
    RESOURCE_ID_ALREADY_EXISTS = (409, "Resource ID is already used.")

    @property
    def status(self) -> str:
        return self.name

    @property
    def http_code(self) -> int:
        return self.value[0]

    @property
    def message(self) -> str:
        return self.value[1]


class AppException(Exception):
    def __init__(self, code: ErrorCode, message: str = None, details: List[Any] = []):
        self.code = code
        self.message = message
        self.details = details


def setup(app: fastapi.FastAPI):
    """Register exception handlers for each type of exception.

    Args:
      app: FastAPI app instance.
    """

    @app.exception_handler(RequestValidationError)
    async def handle_request_valiation(_, exc):
        details = []
        for item in exc.errors():
            details.append({
                'location': item['loc'],
                'message': item['msg'],
                'type': item['type'],
            })

        error = ErrorCode.INVALID_INPUT
        return responses.JSONResponse({
            'error': {
                'code': error.http_code,
                'message': error.message,
                'status': error.status,
                'details': details,
            }
        }, status_code=error.http_code)

    @app.exception_handler(AppException)
    async def http_exception_handler(_, exc):
        e: AppException = exc
        return responses.JSONResponse({
            'error': {
                'code': e.code.http_code,
                'message': e.message if e.message else e.code.message,
                'status': e.code.status,
                'details': e.details,
            }
        }, status_code=e.code.http_code)
