import unittest
from unittest import mock
import json
from io import StringIO

# Import the functions you want to test

# Function to load user data from the JSON file
def load_user_data():
    filename = "data.json"
    try:
        with open(filename, "r") as file:
            json_data = file.read()
            if json_data:
                return json.loads(json_data)
            else:
                return []
    except IOError:
        print("An error occurred while reading the file.")
        return []

# Function to save user data to the JSON file
def save_user_data(data):
    filename = "data.json"
    try:
        with open(filename, "w") as file:
            json_data = json.dumps(data)
            file.write(json_data)
    except IOError:
        print("An error occurred while writing to the file.")

# Function for user registration
def register_user():
    print("USER REGISTRATION")
    user_name = input("Enter username: ")
    user_password = input("Enter password: ")
    user_age = int(input("Enter age: "))

    # Password validation function
    def is_valid_password(password):
        # Check if the password contains at least one letter, one digit, and one special character
        has_letter = any(char.isalpha() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special_char = any(not char.isalnum() for char in password)

        return has_letter and has_digit and has_special_char

    # Validate the password
    while not is_valid_password(user_password):
        print("Password must contain at least one letter, one digit, and one special character.")
        user_password = input("Enter password: ")

    # Create the data dictionary
    data = {
        "name": user_name,
        "password": user_password,
        "age": user_age
    }

    # Load existing user data
    existing_data = load_user_data()
    if existing_data:
        existing_data.append(data)
    else:
        existing_data = [data]

    # Save updated user data
    save_user_data(existing_data)
    print("Registration successful!")

# Function for user login
def login_user():
    print("USER LOGIN")
    user_name = input("Enter username: ")
    user_password = input("Enter password: ")

    # Load user data
    user_data = load_user_data()

    # Check if the entered username and password match for any user
    if any(user["name"] == user_name and user["password"] == user_password for user in user_data):
        print("Login successful!")
        return True

    print("Invalid credentials.")
    return False


class TestLoginManager(unittest.TestCase):

    @mock.patch("builtins.open", mock.mock_open(read_data='[{"name": "user1", "password": "password123", "age": 25}]'))
    def test_load_user_data(self):
        result = load_user_data()
        self.assertEqual(result, [{"name": "user1", "password": "password123", "age": 25}])

    @mock.patch("builtins.open", side_effect=IOError)
    @mock.patch("builtins.print")
    def test_load_user_data_ioerror(self, mock_print, mock_open):
        result = load_user_data()
        self.assertEqual(result, [])
        mock_print.assert_called_once_with("An error occurred while reading the file.")

    @mock.patch("builtins.open", mock.mock_open())
    def test_save_user_data(self):
        data = [{"name": "user1", "password": "pass1", "age": 20}]
        save_user_data(data)
        handle = mock.mock_open()
        handle().write.assert_called_once_with(json.dumps(data))

    @mock.patch("builtins.open", side_effect=IOError)
    @mock.patch("builtins.print")
    def test_save_user_data_ioerror(self, mock_print, mock_open):
        data = [{"name": "user1", "password": "pass1", "age": 20}]
        save_user_data(data)
        mock_print.assert_called_once_with("An error occurred while writing to the file.")

    @mock.patch("builtins.input", side_effect=["user1", "password123", "password123", "25"])
    @mock.patch("builtins.open", mock.mock_open())
    def test_register_user(self, mock_input, mock_open):
        with mock.patch("sys.stdout", new=StringIO()) as fake_output:
            register_user()
            expected_output = "USER REGISTRATION\nRegistration successful!\n"
            self.assertEqual(fake_output.getvalue(), expected_output)
            handle = mock.mock_open()
            handle().write.assert_called_once_with(json.dumps([{"name": "user1", "password": "password123", "age": 25}]))

    @mock.patch("builtins.input", side_effect=["user1", "wrongpassword"])
    @mock.patch("builtins.open", mock.mock_open(read_data='[{"name": "user1", "password": "password123", "age": 25}]'))
    @mock.patch("builtins.print")
    def test_login_user_invalid_credentials(self, mock_print, mock_input, mock_open):
        result = login_user()
        self.assertFalse(result)
        mock_print.assert_called_once_with("Invalid credentials.")

    @mock.patch("builtins.input", side_effect=["user1", "password123"])
    @mock.patch("builtins.open", mock.mock_open(read_data='[{"name": "user1", "password": "password123", "age": 25}]'))
    @mock.patch("builtins.print")
    def test_login_user_successful(self, mock_print, mock_input, mock_open):
        result = login_user()
        self.assertTrue(result)
        mock_print.assert_called_once_with("Login successful!")


if __name__ == '__main__':
    unittest.main()