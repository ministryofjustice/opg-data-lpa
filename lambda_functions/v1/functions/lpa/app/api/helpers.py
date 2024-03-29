import logging
import os
import json
from flask import request


class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the LogRecord.

    @param dict fmt_dict: Key: logging format attribute pairs. Defaults to {"message": "message"}.
    @param str time_format: time.strftime() format string. Default: "%Y-%m-%dT%H:%M:%S"
    @param str msec_format: Microsecond formatting. Appended at the end. Default: "%s.%03dZ"
    """

    def __init__(
        self,
        fmt_dict: dict = None,
        time_format: str = "%Y-%m-%dT%H:%M:%S",
        msec_format: str = "%s.%03dZ",
    ):
        self.fmt_dict = fmt_dict if fmt_dict is not None else {"message": "message"}
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None

    def usesTime(self) -> bool:
        """
        Overwritten to look for the attribute in the format dict values instead of the fmt string.
        """
        return "asctime" in self.fmt_dict.values()

    def checkKey(self, record, fmt_val):
        """
        Returns the value if it exists or empty string otherwise to avoid key errors
        """
        return record.__dict__[fmt_val] if fmt_val in record.__dict__ else ""

    def formatMessage(self, record) -> dict:
        """
        Overwritten to return a dictionary of the relevant LogRecord attributes instead of a string.
        We avoid KeyError by returning "" if key doesn't exist.
        """
        return {
            fmt_key: self.checkKey(record, fmt_val)
            for fmt_key, fmt_val in self.fmt_dict.items()
        }

    def format(self, record) -> str:
        """
        Mostly the same as the parent's class method, the difference being that a dict is manipulated and dumped as JSON
        instead of a string.
        """
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = self.formatMessage(record)

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        return json.dumps(message_dict, default=str)


def get_event_details_for_logs(status, key, cache_used):
    log_object = {
        "source_ip": request.environ["SOURCE_IP"],
        "user_agent": request.environ["USER_AGENT"],
        "method": request.environ["REQUEST_METHOD"],
        "protocol": request.environ["SERVER_PROTOCOL"],
        "request_uri": request.environ["PATH_INFO"],
        "request_id": request.environ["REQUEST_ID"],
        "status": status,
        "key": key,
        "cache_used": cache_used,
    }
    return log_object


def custom_logger(name):
    json_formatter = JsonFormatter(
        {
            "level": "levelname",
            "timestamp": "asctime",
            "request_id": "request_id",
            "request_uri": "request_uri",
            "identifier": "key",
            "cache_used": "cache_used",
            "message_details": "message",
            "status": "status",
            "logger_name": "name",
            "function_name": "funcName",
            "line_number": "lineno",
            "source_ip": "source_ip",
            "user_agent": "user_agent",
            "method": "method",
            "protocol": "protocol",
        }
    )

    handler = logging.StreamHandler()
    handler.setFormatter(json_formatter)
    logger = logging.getLogger(name)
    try:
        logger.setLevel(os.environ["LOGGER_LEVEL"])
    except KeyError:
        logger.setLevel("INFO")
    logger.handlers.clear()  # Remove existing handlers from the logger
    logger.addHandler(handler)
    logger.propagate = False

    # Switch to basic logging for DEBUG as easier to read
    if logger.level == 10:
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logging.basicConfig()

    return logger
