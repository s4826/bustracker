"""Logging configurations"""
import logging
import os
from logging.config import dictConfig

base_dir = os.path.abspath(os.path.dirname(__file__))

if not os.path.exists(f"{base_dir}/logs"):
    os.mkdir(f"{base_dir}/logs")

log_config = {
    "version": 1,
    "formatters": {
        "default": {"format": "%(asctime)s %(levelname)s %(module)s : %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        },
        "debug": {
            "class": "logging.FileHandler",
            "filename": f"{base_dir}/logs/app.debug.log",
            "formatter": "default",
        },
        "error": {
            "class": "logging.FileHandler",
            "filename": f"{base_dir}/logs/app.errors.log",
            "formatter": "default",
        },
    },
    "loggers": {
        "debug": {"handlers": ["debug"], "level": "DEBUG"},
        "error": {"handlers": ["error"], "level": "ERROR"},
    },
    "root": {"level": "DEBUG", "handlers": ["console", "debug"]},
}

dictConfig(log_config)


def get_logger(name):
    return logging.getLogger(name)
