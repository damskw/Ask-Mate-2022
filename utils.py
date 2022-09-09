import config
from datetime import datetime


def quote(arg: str):
    return config.QUOTATION_MARK + arg + config.QUOTATION_MARK


def convert_timestamp_to_utc(timestamp: str or None) -> str or None:
    if timestamp is not None and (isinstance(timestamp, str) or isinstance(timestamp, int)):
        timestamp = int(timestamp)
        # TODO: make sure to save dates in UTC
        date = datetime.utcfromtimestamp(timestamp).strftime("%B %d, %Y")
        return date
    return None
