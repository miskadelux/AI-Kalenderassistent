from datetime import date, datetime, timedelta


def serialize_timedelta(value):
    """Convert a timedelta object to HH:MM:SS."""
    total_seconds = int(value.total_seconds())

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}"



def serialize_value(value):
    """Convert supported Python values to JSON-compatible values."""
    if isinstance(value, timedelta):
        return serialize_timedelta(value)

    if isinstance(value, (date, datetime)):
        return value.isoformat()

    return value


def serialize_data(data):
    """Recursively serialize data into JSON-compatible values."""
    if isinstance(data, dict):
        return {
            key: serialize_data(value)
            for key, value in data.items()
        }

    if isinstance(data, (list, tuple)):
        return [serialize_data(value) for value in data]

    return serialize_value(data)