"""Define helper for test."""
import datetime as dt
import httpx
import basic_app

def get_http_client() -> httpx.AsyncClient:
    """Get an async http client for sending request.

    Returns:
      HTTP client.
    """
    app = basic_app.API()
    return httpx.AsyncClient(
        app=app,
        base_url='http://localhost'
    )

def parse_datetime(time: str) -> dt.datetime:
    return dt.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
