import logging
from datetime import datetime as dt

from data.config import TAG, LOG_FORMAT

now_date = dt.strftime(dt.now(), "%Y-%m-%d %H-%M-%S")

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    filename=f"./logs/{now_date}.txt",
    filemode='a'
)

LOGGER = logging.getLogger(TAG)

# LOGGER.info("GGG")
