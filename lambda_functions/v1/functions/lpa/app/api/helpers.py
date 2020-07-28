import logging
import os


def custom_logger(name=None):
    """
    For consistent logger message formatting

    Args:
        name: string

    Returns:
        Logger instance
    """
    logger_name = name if name else "default"
    formatter = logging.Formatter(
        fmt=f"%(asctime)s - %(levelname)s - {logger_name} - in %("
        f"funcName)s:%(lineno)d - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)

    try:
        logger.setLevel(os.environ["LOGGER_LEVEL"])
    except KeyError:
        logger.setLevel("INFO")
    logger.addHandler(handler)
    return logger
