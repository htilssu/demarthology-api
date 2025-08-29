"""
Simple test for middleware functionality without database dependencies.
"""

import json
import unittest

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.middlewares.camel_case_convert_middleware import CamelCaseConvertMiddleware


class RequestModel(BaseModel):
    first_name: str
    last_name: str
    remember_me: bool = False


class ResponseModel(BaseModel):
    user_info: dict
    total_count: int


class TestCamelCaseMiddlewareSimple(unittest.TestCase):
    """Simple test cases for camelCase conversion middleware."""

    def setUp(self):
        """Set up test app with middleware."""
        # Create a simple test app
        self.app = FastAPI()

        # Add our middleware
        self.app.add_middleware(CamelCaseConvertMiddleware)

        # Create test router
        router = APIRouter()

        @router.post("/test")
        async def test_endpoint(data: RequestModel):
            """Test endpoint that returns snake_case response."""
            return {
                "user_info": {"first_name": data.first_name, "last_name": data.last_name, "remember_me": data.remember_me},
                "total_count": 1,
                "success": True,
            }

        self.app.include_router(router)
        self.client = TestClient(self.app)

    def test_middleware_converts_camelcase_request_to_snakecase(self):
        """Test that middleware converts camelCase request to snake_case."""
        # Send request with camelCase fields
        camel_case_request = {"firstName": "John", "lastName": "Doe", "rememberMe": True}

        response = self.client.post("/test", json=camel_case_request, headers={"Content-Type": "application/json"})

        # Should succeed because middleware converts camelCase to snake_case
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data["userInfo"]["firstName"], "John")
        self.assertEqual(response_data["userInfo"]["lastName"], "Doe")
        self.assertEqual(response_data["userInfo"]["rememberMe"], True)

    def test_middleware_converts_snakecase_response_to_camelcase(self):
        """Test that middleware converts snake_case response to camelCase."""
        request_data = {"firstName": "Jane", "lastName": "Smith", "rememberMe": False}

        response = self.client.post("/test", json=request_data, headers={"Content-Type": "application/json"})

        self.assertEqual(response.status_code, 200)

        # Check that response has camelCase fields
        response_data = response.json()

        # These should be converted from snake_case to camelCase
        self.assertIn("userInfo", response_data)
        self.assertIn("totalCount", response_data)
        self.assertIn("success", response_data)

        # Check nested object conversion
        user_info = response_data["userInfo"]
        self.assertIn("firstName", user_info)
        self.assertIn("lastName", user_info)
        self.assertIn("rememberMe", user_info)

        self.assertEqual(user_info["firstName"], "Jane")
        self.assertEqual(user_info["lastName"], "Smith")
        self.assertEqual(user_info["rememberMe"], False)

    def test_middleware_handles_non_json_content_type(self):
        """Test that middleware doesn't affect non-JSON requests."""
        response = self.client.post(
            "/test", data="firstName=John&lastName=Doe", headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        # Should return 422 because Pydantic expects JSON, but no middleware errors
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
