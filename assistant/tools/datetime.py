from datetime import datetime


def get_current_datetime():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
