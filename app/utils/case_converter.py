"""
Utility functions for converting between camelCase and snake_case.
"""

import re
from typing import Any, Dict, List, Union


def camel_to_snake(name: str) -> str:
    """
    Convert camelCase string to snake_case.

    Args:
        name: camelCase string

    Returns:
        snake_case string

    Examples:
        >>> camel_to_snake("firstName")
        'first_name'
        >>> camel_to_snake("rememberMe")
        'remember_me'
        >>> camel_to_snake("isUserLoggedIn")
        'is_user_logged_in'
    """
    # Handle edge cases
    if not name or not isinstance(name, str):
        return name

    # Insert underscore before uppercase letters that follow lowercase letters
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Insert underscore before uppercase letters that are followed by lowercase letters
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(name: str) -> str:
    """
    Convert snake_case string to camelCase.

    Args:
        name: snake_case string

    Returns:
        camelCase string

    Examples:
        >>> snake_to_camel("first_name")
        'firstName'
        >>> snake_to_camel("remember_me")
        'rememberMe'
        >>> snake_to_camel("is_user_logged_in")
        'isUserLoggedIn'
    """
    # Handle edge cases
    if not name or not isinstance(name, str):
        return name

    components = name.split("_")
    # Keep the first component lowercase and capitalize the rest
    return components[0] + "".join(word.capitalize() for word in components[1:])


def convert_dict_keys_to_snake(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """
    Recursively convert all keys in a dictionary from camelCase to snake_case.

    Args:
        data: Data structure to convert (dict, list, or primitive)

    Returns:
        Data structure with converted keys
    """
    if isinstance(data, dict):
        return {camel_to_snake(key): convert_dict_keys_to_snake(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_dict_keys_to_snake(item) for item in data]
    else:
        return data


def convert_dict_keys_to_camel(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """
    Recursively convert all keys in a dictionary from snake_case to camelCase.

    Args:
        data: Data structure to convert (dict, list, or primitive)

    Returns:
        Data structure with converted keys
    """
    if isinstance(data, dict):
        return {snake_to_camel(key): convert_dict_keys_to_camel(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_dict_keys_to_camel(item) for item in data]
    else:
        return data
