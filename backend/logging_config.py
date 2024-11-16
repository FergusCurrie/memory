log_level = "DEBUG"
log_path = "logs"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"standard": {"format": "{asctime} {levelname} {name} {message}", "style": "{"}},
    "handlers": {
        "console": {"level": log_level, "class": "logging.StreamHandler", "formatter": "standard", "filters": []},
        "backend": {
            "level": log_level,
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": f"{log_path}/backend.log",
        },
        "routes": {
            "level": log_level,
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": f"{log_path}/backend_routes.log",
        },
        "scheduling": {
            "level": log_level,
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": f"{log_path}/backend_scheduling.log",
        },
        "code_execution": {
            "level": log_level,
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": f"{log_path}/backend_code_execution.log",
        },
        # "file_backend": {
        #     "level": log_level,
        #     "class": "logging.FileHandler",
        #     "formatter": "standard",
        #     "filename": f"{log_path}/backend.log",
        # },
    },
    "loggers": {
        "": {  # catch all. all logs go here
            "level": log_level,
            "handlers": ["backend"],
        },
        "backend.scheduling": {  # hierarchial. will only save all api logs
            "level": log_level,
            "handlers": ["scheduling"],
        },
        "backend.code_execution": {  # hierarchial. will only save to api.views logs
            "level": log_level,
            "handlers": ["code_execution"],
        },
        "backend.routes": {  # hierarchial. will only save to api.views logs
            "level": log_level,
            "handlers": ["routes"],
        },
    },
}
