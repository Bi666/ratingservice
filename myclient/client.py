#!/usr/bin/env python3

import argparse
import requests
import getpass
import os
import sys


class ProfessorRatingClient:
    def __init__(self):
        self.token = None
        self.base_url = None

    def check_base_url(self):
        """Check if base_url is set, try to load it if not"""
        if not self.base_url:
            if os.path.exists(".base_url"):
                with open(".base_url", "r") as f:
                    self.base_url = f.read().strip()
            else:
                print("Please login first to set the server URL.")
                return False
        return True

    def load_token(self):
        """Load token from local file"""
        if os.path.exists(".token"):
            with open(".token", "r") as f:
                self.token = f.read().strip()
        if os.path.exists(".base_url"):
            with open(".base_url", "r") as f:
                self.base_url = f.read().strip()

    def require_login(self):
        """Check if user is logged in"""
        self.load_token()
        if not self.token:
            print("You must login first to perform this operation.")
            return False
        if not self.base_url:
            print("Server URL not set. Please login first.")
            return False
        return True

    def register(self):
        """Register a new user"""
        if not self.check_base_url():
            print("Please login first to set the server URL before registering.")
            return

        username = input("Enter username: ")
        email = input("Enter email: ")
        password = getpass.getpass("Enter password: ")

        try:
            response = requests.post(
                f"{self.base_url}/api/register/",
                json={"username": username, "email": email, "password": password}
            )

            if response.status_code == 201:
                print("Registration successful!")
            else:
                print(f"Registration failed: {response.json()}")
        except requests.exceptions.ConnectionError:
            print("Connection error. Please check your internet connection and server availability.")
        except requests.exceptions.Timeout:
            print("Request timed out. Server might be overloaded or unreachable.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def login(self, url):
        """Login to the service"""
        # Auto add http if not present
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        self.base_url = url

        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")

        try:
            response = requests.post(
                f"{self.base_url}/api/login/",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                self.token = response.json()['token']
                # Save token and base_url to local files
                with open(".token", "w") as f:
                    f.write(self.token)
                with open(".base_url", "w") as f:
                    f.write(self.base_url)
                print("Login successful!")
            else:
                print("Login failed. Please check your username and password.")
        except requests.exceptions.ConnectionError:
            print("Connection error. Please check your internet connection and server availability.")
        except requests.exceptions.Timeout:
            print("Request timed out. Server might be overloaded or unreachable.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def logout(self):
        """Logout from the service"""
        token_exists = os.path.exists(".token")
        if token_exists:
            os.remove(".token")
            self.token = None

        url_exists = os.path.exists(".base_url")
        if url_exists:
            os.remove(".base_url")
            self.base_url = None

        if token_exists or url_exists:
            print("Logout successful (local credentials removed).")
        else:
            print("You are not logged in.")

    def list_modules(self):
        """List all module instances"""
        if not self.check_base_url():
            return

        try:
            response = requests.get(f"{self.base_url}/api/modules/")
            if response.status_code == 200:
                modules = response.json()
                if not modules:
                    print("No module instances found.")
                    return
                for module in modules:
                    print(f"Code: {module['code']}")
                    print(f"Name: {module['name']}")
                    print(f"Year: {module['year']}")
                    print(f"Semester: {module['semester']}")
                    professors = module['professors']
                    professor_str = ", ".join([f"{p['id']}, {p['name']}" for p in professors])
                    print(f"Taught by: {professor_str}")
                    print("-" * 70)
            else:
                print(f"Failed to retrieve module list: {response.status_code}")
                if response.status_code == 401:
                    print("You may need to login first.")
        except requests.exceptions.ConnectionError:
            print("Connection error. Please check your internet connection and server availability.")
        except requests.exceptions.Timeout:
            print("Request timed out. Server might be overloaded or unreachable.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def view_ratings(self):
        """View all professor ratings"""
        if not self.check_base_url():
            return

        try:
            response = requests.get(f"{self.base_url}/api/professors/ratings/")
            if response.status_code == 200:
                ratings = response.json()
                if not ratings:
                    print("No professor ratings found.")
                    return
                for prof in ratings:
                    stars = "*" * prof['rating']
                    print(f"The rating of Professor {prof['name']} ({prof['id']}) is {stars}")
            else:
                print(f"Failed to retrieve ratings: {response.status_code}")
                if response.status_code == 401:
                    print("You may need to login first.")
        except requests.exceptions.ConnectionError:
            print("Connection error. Please check your internet connection and server availability.")
        except requests.exceptions.Timeout:
            print("Request timed out. Server might be overloaded or unreachable.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def view_average(self, professor_id, module_code):
        """View average rating of a professor in a module"""
        if not self.check_base_url():
            return

        try:
            response = requests.get(f"{self.base_url}/api/professors/{professor_id}/modules/{module_code}/rating/")
            if response.status_code == 200:
                rating = response.json()['rating']
                stars = "*" * rating
                print(f"The rating of Professor {professor_id} in module {module_code} is {stars}")
            elif response.status_code == 404:
                print(f"No ratings found for Professor {professor_id} in module {module_code}.")
            else:
                print(f"Failed to retrieve average rating: {response.status_code}")
                if response.status_code == 401:
                    print("You may need to login first.")
        except requests.exceptions.ConnectionError:
            print("Connection error. Please check your internet connection and server availability.")
        except requests.exceptions.Timeout:
            print("Request timed out. Server might be overloaded or unreachable.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def verify_module_instance(self, professor_id, module_code, year, semester):
        """Verify if a module instance with given professor, year and semester exists"""
        try:
            response = requests.get(f"{self.base_url}/api/modules/")
            if response.status_code == 200:
                modules = response.json()
                # Check if there's a matching module instance
                for module in modules:
                    if module['code'] == module_code:
                        if str(module['year']) == str(year) and str(module['semester']) == str(semester):
                            for prof in module['professors']:
                                if prof['id'] == professor_id:
                                    return True
                print(f"Error: No module instance found for Professor {professor_id} teaching {module_code} in year {year}, semester {semester}.")
                return False
            else:
                print(f"Failed to verify module instance: {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            print("Connection error while verifying module instance.")
            return False

    def rate_professor(self, professor_id, module_code, year, semester, rating):
        """Rate a professor in a specific module instance"""
        # Check base_url first
        if not self.check_base_url():
            return

        # Check login status
        if not self.require_login():
            return

        # Validate rating value
        try:
            rating_value = int(rating)
            if rating_value < 1 or rating_value > 5:
                print("Rating must be between 1 and 5.")
                return
        except ValueError:
            print("Rating must be a number between 1 and 5.")
            return

        # Verify module instance exists
        if not self.verify_module_instance(professor_id, module_code, year, semester):
            return

        headers = {"Authorization": f"Token {self.token}"}
        data = {
            "professor_id": professor_id,
            "module_code": module_code,
            "year": int(year),
            "semester": int(semester),
            "rating": int(rating)
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/rate/",
                json=data,
                headers=headers
            )

            if response.status_code == 200:
                print("Rating submitted successfully!")
            elif response.status_code == 401:
                print("Authentication failed. Please login again.")
                # Optionally clear the token to force re-login
                self.token = None
                if os.path.exists(".token"):
                    os.remove(".token")
            else:
                print(f"Failed to submit rating: {response.json()}")
        except requests.exceptions.ConnectionError:
            print("Connection error. Please check your internet connection and server availability.")
        except requests.exceptions.Timeout:
            print("Request timed out. Server might be overloaded or unreachable.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


def main():
    client = ProfessorRatingClient()

    parser = argparse.ArgumentParser(description="Professor Rating Client")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Register
    subparsers.add_parser("register", help="Register a new user")

    # Login
    login_parser = subparsers.add_parser("login", help="Login to the service")
    login_parser.add_argument("url", help="URL of the service (e.g., yourusername.pythonanywhere.com)")

    # Logout
    subparsers.add_parser("logout", help="Logout from the service")

    # List
    subparsers.add_parser("list", help="List all module instances")

    # View ratings
    subparsers.add_parser("view", help="View all professor ratings")

    # Average
    average_parser = subparsers.add_parser("average", help="View average rating")
    average_parser.add_argument("professor_id", help="Professor ID")
    average_parser.add_argument("module_code", help="Module code")

    # Rate
    rate_parser = subparsers.add_parser("rate", help="Rate a professor")
    rate_parser.add_argument("professor_id", help="Professor ID")
    rate_parser.add_argument("module_code", help="Module code")
    rate_parser.add_argument("year", help="Teaching year")
    rate_parser.add_argument("semester", help="Semester number")
    rate_parser.add_argument("rating", help="Rating (1-5)")

    args = parser.parse_args()

    if args.command == "register":
        client.register()

    elif args.command == "login":
        client.login(args.url)

    elif args.command == "logout":
        client.logout()

    elif args.command == "list":
        client.list_modules()

    elif args.command == "view":
        client.view_ratings()

    elif args.command == "average":
        client.view_average(args.professor_id, args.module_code)

    elif args.command == "rate":
        client.rate_professor(args.professor_id, args.module_code, args.year, args.semester, args.rating)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()