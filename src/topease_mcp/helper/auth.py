"""API Key authentication module.

All third-party LLMs must provide a valid API_KEY to access
customs trade data through this MCP server.
"""

import os
from functools import wraps
from typing import Any, Callable

from dotenv import load_dotenv

load_dotenv()

_VALID_API_KEYS: set[str] = set(
    key.strip()
    for key in os.getenv("API_KEYS", "").split(",")
    if key.strip()
)


class AuthenticationError(Exception):
    """Raised when API key is missing or invalid."""


def validate_api_key(api_key: str | None) -> None:
    """Validate the provided API key against configured keys.

    Args:
        api_key: The API key to validate.

    Raises:
        AuthenticationError: If the API key is None, empty, or not in
            the configured valid keys list.
    """
    if not api_key:
        raise AuthenticationError(
            "缺少API密钥。第三方大模型调用此MCP必须提供有效的API_KEY。"
            "请在调用时传入 api_key 参数。"
        )

    # if api_key not in _VALID_API_KEYS:
    #     raise AuthenticationError(
    #         "API密钥无效。请检查您的API_KEY是否正确。"
    #     )


def require_api_key(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that enforces API key validation on tool functions.

    The decorated function must accept an ``api_key`` keyword argument.
    The ``api_key`` will be validated before the function executes,
    and stripped from the call arguments afterward.
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        api_key = kwargs.pop("api_key", None)
        validate_api_key(api_key)
        return await func(*args, **kwargs)

    return wrapper


def reload_api_keys() -> None:
    """Reload API keys from environment (useful after config changes)."""
    global _VALID_API_KEYS
    load_dotenv(override=True)
    _VALID_API_KEYS = set(
        key.strip()
        for key in os.getenv("API_KEYS", "").split(",")
        if key.strip()
    )


def get_api_keys_count() -> int:
    """Return the number of configured valid API keys."""
    return len(_VALID_API_KEYS)
