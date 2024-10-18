import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "cargo": {
            "handlers": [
                "cargoLog",
            ],
            "level": "WARNING",
        },
        "colab": {
            "handlers": [
                "colabLog",
            ],
            "level": "WARNING",
        },
        "agrupador": {
            "handlers": [
                "agrupadorLog",
            ],
            "level": "WARNING",
        },
        "observacao": {  #
            "handlers": [
                "observacaoLog",
            ],
            "level": "WARNING",
        },
        "ficha": {
            "handlers": [
                "fichaLog",
            ],
            "level": "WARNING",
        },
        "sgg": {
            "handlers": [
                "sggLog",
            ],
            "level": "WARNING",
        },
        "termo": {
            "handlers": [
                "termoLog",
            ],
            "level": "WARNING",
        },
    },
    "handlers": {
        "cargoLog": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/cargo.log"),
            "formatter": "simpleRe",
        },
        "colabLog": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/colab.log"),
            "formatter": "simpleRe",
        },
        "agrupadorLog": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/colab.log"),
            "formatter": "simpleRe",
        },
        "observacaoLog": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/observacao.log"),
            "formatter": "simpleRe",
        },
        "fichaLog": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/ficha.log"),
            "formatter": "simpleRe",
        },
        "sggLog": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/sgg.log"),
            "formatter": "simpleRe",
        },
        "termoLog": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/termo.log"),
            "formatter": "simpleRe",
        },
    },
    "formatters": {
        "simpleRe": {
            "format": "{levelname} {asctime} {module} {funcName} {lineno} {message}",
            "style": "{",
            "datefmt": "%d/%m/%Y %H:%M:%S",
        }
    },
}
