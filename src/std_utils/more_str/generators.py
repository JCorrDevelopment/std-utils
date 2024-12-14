"""
This module contains any useful utility functions used for string generation.

Functions:
    uuid_to_base64: Generate a random string using the uuid and convert it to base64.
    random_string: Generate a random string based on specified prefix, suffix, and randomizer.
"""

__all__ = [
    "random_string",
    "uuid_to_base64",
]

import base64
import uuid
from collections.abc import Callable
from typing import Literal

from std_utils.more_typing.undefined import DOC_UNDEFINED, is_undefined


def uuid_to_base64(
    uuid_type: Literal["uuid1", "uuid3", "uuid4", "uuid5"] = "uuid4", namespace: str = DOC_UNDEFINED
) -> str:
    """
    Convert a string to a base64 encoded string.

    Parameters:
        uuid_type (str): The type of UUID to generate. Must be one of "uuid1", "uuid3", "uuid4", or "uuid5".
        namespace (str): The namespace to use for the UUID. Only used for "uuid3" and "uuid5" UUID types.

    Returns:
        str: The base64 encoded string.

    Raises:
        ValueError: If the UUID type is invalid;
        ValueError: If the namespace is not provided for "uuid3" and "uuid5" UUID types
    """
    match uuid_type:
        case "uuid1" | "uuid4":
            input_bytes = getattr(uuid, uuid_type)().hex.encode("utf-8")
        case "uuid3" | "uuid5":
            if is_undefined(namespace):
                msg = "Namespace must be provided for 'uuid3' and 'uuid5' UUID types."
                raise ValueError(msg)
            input_bytes = getattr(uuid, uuid_type)(uuid.NAMESPACE_DNS, namespace).hex.encode("utf-8")
        case _:
            msg = f"Invalid UUID type: {uuid_type!r}"
            raise ValueError(msg)
    base64_bytes = base64.b64encode(input_bytes)
    return base64_bytes.decode("utf-8")


def random_string(
    prefix: str = "",
    suffix: str = "",
    randomizer: Callable[[], str] = uuid_to_base64,
    max_length: int = 200,
) -> str:
    """
    Generate a random string.

    Parameters:
        prefix (str | None): Optional prefix to add to the string.
        suffix (str | None): Optional suffix to add to the string.
        randomizer (Callable[[], str] | None): Optional function that will be used to generate the random part of the
            string. If None, the default randomizer will be used.
        max_length (int): Maximum length of the generated string.

    Returns:
        str: Generated random string.

    Raises:
        ValueError: If the generated string is longer than the maximum length.
    """
    if len(result := f"{prefix}{randomizer()}{suffix}") <= max_length:
        return result
    msg = (
        f"Generated string {result!r} is longer than the maximum length of {max_length} characters."
        f"Ensure the randomizer function does not generate too long strings for you or increase the"
        f"`max_length` parameter."
    )
    raise ValueError(msg)
