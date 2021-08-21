"""Define entrypoint here."""

import basic_app
from basic_app import (
    argument,
)

from basic_app.lib import (
    config,
    logging,
    uvicorn,
)

app = None

def main():
    """Our entrypoint."""
    args = argument.parse_args()

    conf = config.setup(args.envfile)

    logging.setup(conf)

    basic_app.setup(conf)

    global app
    app = basic_app.API()

    uvicorn.run(
        "basic_app.__main__:app",
        host=conf.host,
        port=int(conf.port),
    )

if __name__ == "__main__":
    main()
