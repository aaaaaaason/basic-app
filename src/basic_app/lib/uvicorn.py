"""Wrapper for uvicorn"""
import uvicorn

def run(app_location: str, host: str, port: int):
    """Start running uvicore server.

    Args:
      app_location: In "<module>:<func>" format
      host: The server host to run
      port: The port to listen on
    """
    # https://github.com/tiangolo/fastapi/issues/1508
    uvicorn.run(
        app_location,
        host=host,
        port=port,
        log_config=None)
