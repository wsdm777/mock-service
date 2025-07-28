import os
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    log_dir = "/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_filename = datetime.now().strftime("%Y-%m-%d.log")

    log_format = "%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.setLevel(logging.WARNING)
    sqlalchemy_logger.propagate = False

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))
    stream_handler.setLevel(logging.INFO)

    logger.addHandler(stream_handler)

    file_handler = TimedRotatingFileHandler(
        os.path.join(log_dir, log_filename),
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
    )

    file_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))
    logger.addHandler(file_handler)
