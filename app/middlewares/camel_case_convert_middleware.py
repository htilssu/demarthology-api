"""
Middleware for converting camelCase to snake_case in requests and snake_case to camelCase in responses.
"""

import json
from typing import Callable

from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.utils.case_converter import (
    convert_dict_keys_to_camel,
    convert_dict_keys_to_snake,
)


class CamelCaseConvertMiddleware:
    """
    ASGI middleware that converts:
    - Incoming request JSON keys from camelCase to snake_case
    - Outgoing response JSON keys from snake_case to camelCase
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        """
        ASGI application interface.

        Args:
            scope: ASGI scope
            receive: ASGI receive callable
            send: ASGI send callable
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Wrap receive to convert request body
        async def receive_wrapper():
            message = await receive()
            if message["type"] == "http.request":
                body = message.get("body", b"")
                if body:
                    # Convert request body keys from camelCase to snake_case
                    converted_body = await self._convert_request_body(body, scope)
                    if converted_body is not None:
                        message["body"] = converted_body
            return message

        # Wrap send to convert response body
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = [(k, v) for k, v in message["headers"] if k.lower() != b"content-length"]
                message["headers"] = headers

            if message["type"] == "http.response.body":
                body = message.get("body", b"")
                if body:
                    # Convert response body keys from snake_case to camelCase
                    converted_body = await self._convert_response_body(body)
                    if converted_body is not None:
                        message["body"] = converted_body
                headers = scope["headers"]

            await send(message)

        await self.app(scope, receive_wrapper, send_wrapper)

    async def _convert_request_body(self, body: bytes, scope: dict) -> bytes:
        """
        Convert request JSON keys from camelCase to snake_case.

        Args:
            body: Request body bytes
            scope: ASGI scope containing headers

        Returns:
            Converted body bytes or None if no conversion needed
        """
        try:
            # Check content type
            headers = dict(scope.get("headers", []))
            content_type = headers.get(b"content-type", b"").decode("utf-8")

            if not content_type.startswith("application/json"):
                return None

            if not body:
                return None

            # Parse JSON
            data = json.loads(body.decode("utf-8"))

            # Convert camelCase keys to snake_case
            converted_data = convert_dict_keys_to_snake(data)

            # Return new body
            return json.dumps(converted_data).encode("utf-8")

        except (json.JSONDecodeError, UnicodeDecodeError):
            # If JSON parsing fails, return None (no conversion)
            return None

    async def _convert_response_body(self, body: bytes) -> bytes:
        """
        Convert response JSON keys from snake_case to camelCase.

        Args:
            body: Response body bytes

        Returns:
            Converted body bytes or None if no conversion needed
        """
        try:
            if not body:
                return None

            # Parse JSON
            data = json.loads(body.decode("utf-8"))

            # Convert snake_case keys to camelCase
            converted_data = convert_dict_keys_to_camel(data)

            # Return new body
            return json.dumps(converted_data).encode("utf-8")

        except (json.JSONDecodeError, UnicodeDecodeError):
            # If JSON parsing fails, return None (no conversion)
            return None
