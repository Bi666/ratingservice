# client.py

import argparse
import requests
import getpass
import sys
import json


class ProfessorRatingClient:
    def __init__(self):
        self.token = None
        self.base_url = "http://127.0.0.1:8000"  # Default to local development server

    def register(self):
        if not self.base_url:
            print("Error: No server URL specified. Use 'login <url>' first or specify URL with register command.")
            return False

        username = input("Enter username: ")
        email = input("Enter email: ")
        password = getpass.getpass("Enter password: ")

        response = requests.post(
            f"{self.base_url}/api/register/",
            json={"username": username, "email": email, "password": password}
        )

        if response.status_code == 201:
            self.token = response.json()['token']
            print("Registration successful! You are now logged in.")
            return True
        else:
            print(f"Registration failed: {response.json()}")
            return False

    def login(self, url):
        # If URL doesn't start with http:// or https://, add http://
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"http://{url}"

        self.base_url = url
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")

        response = requests.post(
            f"{self.base_url}/api/login/",
            json={"username": username, "password": password}
        )

        if response.status_code == 200:
            self.token = response.json()['token']
            print("Login successful!")
            return True
        else:
            print("Login failed. Please check your username and password.")
            return False

    def logout(self):
        if not self.token:
            print("You are not logged in!")
            return

        headers = {"Authorization": f"Token {self.token}"}
        response = requests.post(f"{self.base_url}/api/logout/", headers=headers)

        if response.status_code == 200:
            self.token = None
            print("Logout successful!")
        else:
            print("Logout failed.")

    def list_modules(self):
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
            print("Failed to retrieve module list.")

    def view_ratings(self):
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
            print("Failed to retrieve ratings.")

    def view_average(self, professor_id, module_code):
        response = requests.get(
            f"{self.base_url}/api/professors/{professor_id}/modules/{module_code}/rating/"
        )

        if response.status_code == 200:
            rating = response.json()['rating']
            stars = "*" * rating
            print(f"The rating of Professor {professor_id} in module {module_code} is {stars}")
        else:
            print("Failed to retrieve average rating.")

    def rate_professor(self, professor_id, module_code, year, semester, rating):
        if not self.token:
            print("You need to log in first to rate professors!")
            return

        if not (1 <= int(rating) <= 5):
            print("Rating must be between 1 and 5.")
            return

        headers = {"Authorization": f"Token {self.token}"}
        data = {
            "professor_id": professor_id,
            "module_code": module_code,
            "year": int(year),
            "semester": int(semester),
            "rating": int(rating)
        }

        response = requests.post(
            f"{self.base_url}/api/rate/",
            json=data,
            headers=headers
        )

        if response.status_code == 200:
            print("Rating submitted successfully!")
        else:
            print(f"Failed to submit rating: {response.json()}")


def main():
    client = ProfessorRatingClient()

    parser = argparse.ArgumentParser(description="Professor Rating Client")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Register command
    register_parser = subparsers.add_parser("register", help="Register a new user")
    register_parser.add_argument("--url", help="URL of the service (e.g., yourusername.pythonanywhere.com)",
                                 default="127.0.0.1:8000")

    # Login command
    login_parser = subparsers.add_parser("login", help="Log in to the service")
    login_parser.add_argument("url", help="URL of the service (e.g., yourusername.pythonanywhere.com)")

    # Logout command
    subparsers.add_parser("logout", help="Log out from the service")

    # List modules command
    subparsers.add_parser("list", help="List all module instances")

    # View ratings command
    subparsers.add_parser("view", help="View ratings of all professors")

    # View average rating command
    average_parser = subparsers.add_parser("average", help="View average rating of a professor in a module")
    average_parser.add_argument("professor_id", help="Professor ID")
    average_parser.add_argument("module_code", help="Module code")

    # Rate command
    rate_parser = subparsers.add_parser("rate", help="Rate a professor")
    rate_parser.add_argument("professor_id", help="Professor ID")
    rate_parser.add_argument("module_code", help="Module code")
    rate_parser.add_argument("year", help="Teaching year")
    rate_parser.add_argument("semester", help="Semester number (1 or 2)")
    rate_parser.add_argument("rating", help="Rating (1-5)")

    args = parser.parse_args()

    if args.command == "register":
        if hasattr(args, 'url') and args.url:
            client.base_url = f"http://{args.url}"
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