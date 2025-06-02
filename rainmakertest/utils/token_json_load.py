import json
from typing import Any, Union


def prettify(
        data: Union[dict, list, str, bytes],
        indent: int = 2,
        sort_keys: bool = True,
        ensure_ascii: bool = False
) -> str:
    """
    Convert JSON data to a nicely formatted string with proper indentation.

    Args:
        data: JSON data to format (can be dict, list, str, or bytes)
        indent: Number of spaces for indentation
        sort_keys: Whether to sort dictionary keys alphabetically
        ensure_ascii: Escape non-ASCII characters when True

    Returns:
        Formatted JSON string

    Raises:
        ValueError: If input data cannot be converted to valid JSON
    """
    try:
        # Handle bytes input
        if isinstance(data, bytes):
            data = data.decode('utf-8')

        # Parse string input
        if isinstance(data, str):
            parsed = json.loads(data)
        else:
            parsed = data

        # Format with given parameters
        return json.dumps(
            parsed,
            indent=indent,
            sort_keys=sort_keys,
            ensure_ascii=ensure_ascii,
            separators=(',', ': ')
        )

    except (TypeError, json.JSONDecodeError) as e:
        raise ValueError(f"Invalid JSON data: {str(e)}") from e


def validate_json(data: Union[dict, list, str, bytes]) -> bool:
    """
    Validate if input is valid JSON data.

    Args:
        data: Input data to validate

    Returns:
        True if valid JSON, False otherwise
    """
    try:
        if isinstance(data, (dict, list)):
            json.dumps(data)
            return True
        if isinstance(data, (str, bytes)):
            json.loads(data if isinstance(data, str) else data.decode('utf-8'))
            return True
        return False
    except (TypeError, ValueError, json.JSONDecodeError):
        return False


if __name__ == "__main__":
    # Example usage
    sample_data = {
        "name": "ESP RainMaker",
        "version": "1.0",
        "features": ["OTA", "Cloud", "MQTT"],
        "config": {"timeout": 30, "retries": 3}
    }

    print("Pretty JSON:")
    print(prettify(sample_data))

    print("\nValidation Test:")
    print(f"Is valid: {validate_json(sample_data)}")
    print(f"Is valid: {validate_json('invalid')}")