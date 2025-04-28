PROFESSOR RATING SERVICE - CLIENT INSTRUCTIONS
==============================================

REQUIREMENTS:
- Python 3.x
- requests library (install using: pip install requests)

COMMANDS:
---------
1. register
   Usage: python ./myclient/client.py register
   Description: Register a new user account. You will be prompted to enter username, email, and password.

2. login
   Usage: python ./myclient/client.py login URL
   Description: Log in to the service. URL should be your PythonAnywhere domain.
   Example: python ./myclient/client.py login mn21bw.pythonanywhere.com

3. logout
   Usage: python ./myclient/client.py logout
   Description: Log out and remove locally stored credentials.

4. list
   Usage: python ./myclient/client.py list
   Description: List all module instances and professors teaching each module.

5. view
   Usage: python ./myclient/client.py view
   Description: View ratings of all professors.

6. average
   Usage: python ./myclient/client.py average PROFESSOR_ID MODULE_CODE
   Description: View average rating of a professor in a specific module.
   Example: python ./myclient/client.py average JE1 CD1

7. rate
   Usage: python ./myclient/client.py rate PROFESSOR_ID MODULE_CODE YEAR SEMESTER RATING
   Description: Rate a professor (1-5) in a specific module instance. Requires login.
   Example: python ./myclient/client.py rate JE1 CD1 2018 2 5

PYTHONANYWHERE DOMAIN:
---------------------
mn21bw.pythonanywhere.com

ADMIN ACCOUNT CREDENTIALS:
------------------------
Username: mn21bw
Password: wbl20031002

ADDITIONAL INFORMATION:
---------------------
- The client stores authentication tokens in hidden files (.token and .base_url) in the current directory.
- You must be logged in to rate professors.
- When using the rate command, ensure the professor teaches the specified module in the given year and semester.
- The client handles most connection errors and will display appropriate error messages.
- To run the client from any directory, navigate to the project root and use the commands as shown above.