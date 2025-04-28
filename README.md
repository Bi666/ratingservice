# Professor Rating Service - User Guide

## Client Command List

1. **Register a New User**  
   ```bash
   python client.py register
   ```

2. **Login to the System**  
   ```bash
   python client.py login yourusername.pythonanywhere.com
   ```

3. **Logout from the System**  
   ```bash
   python client.py logout
   ```

4. **List All Module Instances and Professors**  
   ```bash
   python client.py list
   ```

5. **View All Professor Ratings**  
   ```bash
   python client.py view
   ```

6. **View the Average Rating for a Specific Professor in a Specific Module**  
   ```bash
   python client.py average PROFESSOR_ID MODULE_CODE
   ```
   Example:  
   ```bash
   python client.py average JE1 CD1
   ```

7. **Rate a Professor**  
   ```bash
   python client.py rate PROFESSOR_ID MODULE_CODE YEAR SEMESTER RATING
   ```
   Example:  
   ```bash
   python client.py rate JE1 CD1 2018 2 5
   ```

## PythonAnywhere Information

- Website URL: `[yourusername].pythonanywhere.com`
- Admin Username & Password: `[your admin credentials]`

## Important Notes

- Python 3.x and the `requests` library are required to run the client.
- Ratings must be between **1 and 5**.
- You must **log in** before submitting a rating.
- You can only rate valid professor-module combinations.
