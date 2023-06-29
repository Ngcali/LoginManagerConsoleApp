import unittest
import json
from unittest.mock import patch
from io import StringIO

import main

class TestLoginManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary data file for testing
        with open("data.json", "w") as file:
            file.write('[]')

    def test_register_user(self):
        # Simulate user input
        user_input = [
            "John",  # username
            "Password1!",  # password
            "25",  # age
        ]

        # Simulate user input using the patch decorator
        with patch("builtins.input", side_effect=user_input):
            # Redirect print statements to StringIO for testing
            with patch("sys.stdout", new=StringIO()) as output:
                main.register_user()

                # Verify the printed output
                expected_output = "USER REGISTRATION\nRegistration successful!\n"
                self.assertEqual(output.getvalue(), expected_output)

        # Load user data from the temporary file
        user_data = main.load_user_data()

        # Verify the user is registered and data is saved correctly
        self.assertEqual(len(user_data), 1)
        self.assertEqual(user_data[0]["name"], "John")
        self.assertEqual(user_data[0]["password"], "Password1!")
        self.assertEqual(user_data[0]["age"], 25)

    def test_login_user(self):
        # Add a test user to the temporary file
        user_data = [
            {
                "name": "John",
                "password": "Password1!",
                "age": 25
            }
        ]
        with open("data.json", "w") as file:
            file.write(json.dumps(user_data))

        # Simulate user input
        user_input = [
            "John",  # username
            "Password1!",  # password
        ]

        # Simulate user input using the patch decorator
        with patch("builtins.input", side_effect=user_input):
            # Redirect print statements to StringIO for testing
            with patch("sys.stdout", new=StringIO()) as output:
                result = main.login_user()

                # Verify the printed output
                expected_output = "USER LOGIN\nLogin successful!\n"
                self.assertEqual(output.getvalue(), expected_output)

        # Verify the login was successful
        self.assertTrue(result)

    def test_invalid_login(self):
        # Add a test user to the temporary file
        user_data = [
            {
                "name": "John",
                "password": "Password1!",
                "age": 25
            }
        ]
        with open("data.json", "w") as file:
            file.write(json.dumps(user_data))

        # Simulate user input
        user_input = [
            "John",  # username
            "WrongPassword",  # password
        ]

        # Simulate user input using the patch decorator
        with patch("builtins.input", side_effect=user_input):
            # Redirect print statements to StringIO for testing
            with patch("sys.stdout", new=StringIO()) as output:
                result = main.login_user()

                # Verify the printed output
                expected_output = "USER LOGIN\nInvalid credentials.\n"
                self.assertEqual(output.getvalue(), expected_output)

        # Verify the login was unsuccessful
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
