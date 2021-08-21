"""Try Google signin."""

import logging
from fastapi import (
    APIRouter,
    Cookie,
    Form,
    Request,
    responses,
)
from fastapi.templating import Jinja2Templates
from google.oauth2 import id_token
from google.auth.transport import requests

from basic_app.lib import exception

router = APIRouter()

_controller = None

_templates = Jinja2Templates(directory="./src/basic_app/templates")

@router.get("/google-signin", response_class=responses.HTMLResponse)
async def signin_view(request: Request):
    return await _controller.signin_view(request)

@router.post("/google-signin")
async def google_signin(credential: str = Form(None),
    csrf_token: str = Form(None),
    csrf_cookie: str = Cookie(None)):
    return await _controller.google_signin(credential, csrf_token, csrf_cookie)

class GoogleSignin:
    """Define router."""

    def __init__(self, app_host: str, client_id: str):
        global _controller
        _controller = self
        self._app_host = app_host
        self._client_id = client_id

    async def signin_view(self, request: Request):
        """The entrypoint of GET /google-signin request."""
        return _templates.TemplateResponse('google-signin.html', {
            "request": request,
            "google_client_id": self._client_id,
            "app_host": self._app_host,
        })

    async def google_signin(self, credential, csrf_token, csrf_cookie):
        """The entrypoint of POST /google-signin request."""
        if not csrf_cookie:
            exception.AppException(
                code=exception.ErrorCode.INVALID_INPUT,
                message="No CSRF token in Cookie.",
            )
        if not csrf_token:
            exception.AppException(
                code=exception.ErrorCode.INVALID_INPUT,
                message="No CSRF token in body.",
            )
        if csrf_cookie != csrf_token:
            exception.AppException(
                code=exception.ErrorCode.INVALID_INPUT,
                message="Failed to verify double submit cookie.",
            )

        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            _ = id_token.verify_oauth2_token(credential, requests.Request(), self._client_id)
            logging.info("Sign in succeeded.")
            # TODO: Save user into database and create session.
        except ValueError:
            raise exception.AppException(
                code=exception.ErrorCode.AUTHENTICATION_FAIL,
                message="Failed to verify ID token.",
            )
