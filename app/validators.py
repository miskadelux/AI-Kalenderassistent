
import re
from datetime import date


def validate_date(value, parameter_name):
    """
    Validate a date string using the exact YYYY-MM-DD format.

    Returns:
        date: The validated date.

    Raises:
        ValueError: If the value does not match YYYY-MM-DD
                    or represents an invalid date.
    """
    if not isinstance(value, str):
        raise TypeError(f"Parameter {parameter_name} måste vara ett datum.")

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(
            f"Parameter {parameter_name} måste ha formatet YYYY-MM-DD."
        )

    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(
            f"Parameter {parameter_name} innehåller ett ogiltigt datum."
        ) from None



def validate_date_range(start_date, end_date):
    """
    Validate that the start date is not later than the end date.

    Raises:
        ValueError: If start_date is later than end_date.
    """
    if start_date is not None and end_date is not None and start_date > end_date:
        raise ValueError(
            "start_date får inte vara senare än end_date."
        )
