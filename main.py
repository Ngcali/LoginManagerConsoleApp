import json

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

# Function for user login
def login_user():
    print("USER LOGIN")
    user_name = input("Enter username: ")
    user_password = input("Enter password: ")

    # Load user data
    user_data = load_user_data()

    # Check if the entered username and password match
    for user in user_data:
        if user["name"] == user_name and user["password"] == user_password:
            print("Login successful!")
            return True

    print("Invalid credentials.")
    return False

# Main program loop
while True:
    print("WELCOME TO LOGIN MANAGER")

    choice = input("Choose an option (1 - Register, 2 - Login, 3 - Exit): ")

    if choice == "1":
        register_user()
    elif choice == "2":
        if login_user():
            break  # Break the loop on successful login
    elif choice == "3":
        print("Exiting the program.")
        break  # Break the loop to exit the program
    else:
        print("Invalid choice. Please try again.")
