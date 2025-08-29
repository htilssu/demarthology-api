"""
Tests for case conversion utilities.
"""
import unittest

from app.utils.case_converter import (
    camel_to_snake,
    snake_to_camel,
    convert_dict_keys_to_snake,
    convert_dict_keys_to_camel
)


class TestCaseConverter(unittest.TestCase):
    """Test cases for case conversion utilities."""

    def test_camel_to_snake_basic(self):
        """Test basic camelCase to snake_case conversion."""
        self.assertEqual(camel_to_snake("firstName"), "first_name")
        self.assertEqual(camel_to_snake("lastName"), "last_name")
        self.assertEqual(camel_to_snake("rememberMe"), "remember_me")
        self.assertEqual(camel_to_snake("isUserLoggedIn"), "is_user_logged_in")

    def test_camel_to_snake_edge_cases(self):
        """Test edge cases for camelCase to snake_case conversion."""
        self.assertEqual(camel_to_snake(""), "")
        self.assertEqual(camel_to_snake("a"), "a")
        self.assertEqual(camel_to_snake("A"), "a")
        self.assertEqual(camel_to_snake("email"), "email")
        self.assertEqual(camel_to_snake("ID"), "id")
        self.assertEqual(camel_to_snake("HTTPResponse"), "http_response")
        self.assertEqual(camel_to_snake(None), None)
        self.assertEqual(camel_to_snake(123), 123)

    def test_snake_to_camel_basic(self):
        """Test basic snake_case to camelCase conversion."""
        self.assertEqual(snake_to_camel("first_name"), "firstName")
        self.assertEqual(snake_to_camel("last_name"), "lastName")
        self.assertEqual(snake_to_camel("remember_me"), "rememberMe")
        self.assertEqual(snake_to_camel("is_user_logged_in"), "isUserLoggedIn")

    def test_snake_to_camel_edge_cases(self):
        """Test edge cases for snake_case to camelCase conversion."""
        self.assertEqual(snake_to_camel(""), "")
        self.assertEqual(snake_to_camel("a"), "a")
        self.assertEqual(snake_to_camel("email"), "email")
        self.assertEqual(snake_to_camel("_private"), "Private")
        self.assertEqual(snake_to_camel("__dunder__"), "Dunder")
        self.assertEqual(snake_to_camel(None), None)
        self.assertEqual(snake_to_camel(123), 123)

    def test_convert_dict_keys_to_snake_simple(self):
        """Test dictionary key conversion to snake_case."""
        input_dict = {
            "firstName": "John",
            "lastName": "Doe",
            "rememberMe": True
        }
        expected = {
            "first_name": "John",
            "last_name": "Doe",
            "remember_me": True
        }
        result = convert_dict_keys_to_snake(input_dict)
        self.assertEqual(result, expected)

    def test_convert_dict_keys_to_snake_nested(self):
        """Test nested dictionary key conversion to snake_case."""
        input_dict = {
            "userInfo": {
                "firstName": "John",
                "lastName": "Doe",
                "contactInfo": {
                    "emailAddress": "john@example.com",
                    "phoneNumber": "123-456-7890"
                }
            },
            "rememberMe": True
        }
        expected = {
            "user_info": {
                "first_name": "John",
                "last_name": "Doe",
                "contact_info": {
                    "email_address": "john@example.com",
                    "phone_number": "123-456-7890"
                }
            },
            "remember_me": True
        }
        result = convert_dict_keys_to_snake(input_dict)
        self.assertEqual(result, expected)

    def test_convert_dict_keys_to_snake_with_lists(self):
        """Test dictionary with lists key conversion to snake_case."""
        input_dict = {
            "userList": [
                {"firstName": "John", "lastName": "Doe"},
                {"firstName": "Jane", "lastName": "Smith"}
            ],
            "totalCount": 2
        }
        expected = {
            "user_list": [
                {"first_name": "John", "last_name": "Doe"},
                {"first_name": "Jane", "last_name": "Smith"}
            ],
            "total_count": 2
        }
        result = convert_dict_keys_to_snake(input_dict)
        self.assertEqual(result, expected)

    def test_convert_dict_keys_to_camel_simple(self):
        """Test dictionary key conversion to camelCase."""
        input_dict = {
            "first_name": "John",
            "last_name": "Doe",
            "remember_me": True
        }
        expected = {
            "firstName": "John",
            "lastName": "Doe",
            "rememberMe": True
        }
        result = convert_dict_keys_to_camel(input_dict)
        self.assertEqual(result, expected)

    def test_convert_dict_keys_to_camel_nested(self):
        """Test nested dictionary key conversion to camelCase."""
        input_dict = {
            "user_info": {
                "first_name": "John",
                "last_name": "Doe",
                "contact_info": {
                    "email_address": "john@example.com",
                    "phone_number": "123-456-7890"
                }
            },
            "remember_me": True
        }
        expected = {
            "userInfo": {
                "firstName": "John",
                "lastName": "Doe",
                "contactInfo": {
                    "emailAddress": "john@example.com",
                    "phoneNumber": "123-456-7890"
                }
            },
            "rememberMe": True
        }
        result = convert_dict_keys_to_camel(input_dict)
        self.assertEqual(result, expected)

    def test_convert_dict_keys_to_camel_with_lists(self):
        """Test dictionary with lists key conversion to camelCase."""
        input_dict = {
            "user_list": [
                {"first_name": "John", "last_name": "Doe"},
                {"first_name": "Jane", "last_name": "Smith"}
            ],
            "total_count": 2
        }
        expected = {
            "userList": [
                {"firstName": "John", "lastName": "Doe"},
                {"firstName": "Jane", "lastName": "Smith"}
            ],
            "totalCount": 2
        }
        result = convert_dict_keys_to_camel(input_dict)
        self.assertEqual(result, expected)

    def test_convert_non_dict_data(self):
        """Test conversion with non-dictionary data."""
        # Test with primitive values
        self.assertEqual(convert_dict_keys_to_snake("string"), "string")
        self.assertEqual(convert_dict_keys_to_snake(123), 123)
        self.assertEqual(convert_dict_keys_to_snake(True), True)
        self.assertEqual(convert_dict_keys_to_snake(None), None)
        
        self.assertEqual(convert_dict_keys_to_camel("string"), "string")
        self.assertEqual(convert_dict_keys_to_camel(123), 123)
        self.assertEqual(convert_dict_keys_to_camel(True), True)
        self.assertEqual(convert_dict_keys_to_camel(None), None)

        # Test with lists of primitives
        input_list = ["item1", "item2", 123]
        self.assertEqual(convert_dict_keys_to_snake(input_list), input_list)
        self.assertEqual(convert_dict_keys_to_camel(input_list), input_list)

    def test_round_trip_conversion(self):
        """Test that converting camelCase to snake_case and back preserves the original."""
        original = {
            "firstName": "John",
            "lastName": "Doe",
            "userInfo": {
                "emailAddress": "john@example.com",
                "isActive": True
            }
        }
        
        # Convert to snake_case then back to camelCase
        snake_case = convert_dict_keys_to_snake(original)
        back_to_camel = convert_dict_keys_to_camel(snake_case)
        
        self.assertEqual(original, back_to_camel)


if __name__ == "__main__":
    unittest.main()