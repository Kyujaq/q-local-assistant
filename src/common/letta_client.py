"""Letta client configuration and wrapper."""

import os
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class LettaConfig(BaseSettings):
    """Configuration for Letta client connection."""

    base_url: str = Field(
        default="http://localhost:8283",
        description="Base URL for Letta server",
    )
    api_token: Optional[str] = Field(
        default=None,
        description="API token for authentication (if required)",
    )
    timeout: int = Field(
        default=300,
        description="Request timeout in seconds",
    )

    model_config = {
        "env_prefix": "LETTA_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


def get_letta_client():
    """
    Get a configured Letta client instance.

    Returns:
        Configured Letta client

    Raises:
        ImportError: If letta package is not installed
        ConnectionError: If cannot connect to Letta server
    """
    try:
        from letta import Letta
    except ImportError as e:
        raise ImportError(
            "letta package not installed. Install with: pip install letta"
        ) from e

    config = LettaConfig()

    client_kwargs = {"base_url": config.base_url}
    if config.api_token:
        client_kwargs["token"] = config.api_token

    try:
        client = Letta(**client_kwargs)
        return client
    except Exception as e:
        raise ConnectionError(
            f"Failed to connect to Letta server at {config.base_url}: {e}"
        ) from e
