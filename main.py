import logging.config
import config
import os
import yaml
from fastapi import FastAPI

from temu.api.endpoints import payment, order_update, check_status, callback

PREFIX = "/test-emulator"

temu = FastAPI()
temu.include_router(payment.router, prefix=PREFIX)
temu.include_router(order_update.router, prefix=PREFIX)
temu.include_router(check_status.router, prefix=PREFIX)
temu.include_router(callback.router, prefix=PREFIX)


def setup_logging() -> None:
    config_path = os.path.join('temu', 'settings', 'log_config.yaml')

    try:
        with open(config_path, 'rt') as config_file:
            log_config = yaml.safe_load(config_file.read())
        logging.config.dictConfig(log_config)
    except Exception as e:
        logging.basicConfig(level=logging.WARN)
        logging.error("Error at logging config load: %s", e)


setup_logging()
logger = logging.getLogger(__name__)


@temu.get("/")
def read_root():
    logger.info("Incoming request to the main page")
    return {"message": "Welcome to test emulator"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(temu, host="127.0.0.1", port=8000)
