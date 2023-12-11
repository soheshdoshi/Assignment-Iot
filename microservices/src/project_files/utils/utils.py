"""
utils.py create for basic utils purpose.
"""

from typing import Any


def check_str(name: Any) -> bool:
    """
    check_str for check value is str or not body parameter validation purpose.
    """
    if not isinstance(name, str):
        return False
    return True


def check_value(value: Any) -> bool:
    """
    check_value for check value is float or not body parameter validation purpose.
    """
    if not isinstance(value, float):
        return False
    return True
