import re

def validate_password(password, email, confirm_password):
    if password != confirm_password:
            return "Passwords do not match.", 400

    if len(password) < 8:
        return "passowrd must be at least 8 characters", 400
    elif not any(char.isupper() for char in password):
        return "Password must include at least one uppercase letter.", 400
    elif not any(char.islower() for char in password):
        return "Password must include at least one lowercase letter.", 400
    elif not any(char.isdigit() for char in password):
        return "Password must include at least one number.", 400
    elif not any(char in "!@#$%^&*()_+-=[]{};':\",.<>?/\\|" for char in password):
        return "Password must include at least one special character.", 400
    elif " " in password:
        return "Password must not contain spaces.", 400


    common_password = ["0000000", "12345678", "abcd", "abc123"]
    if password.lower() in common_password:
        return "Password is too common, choose a stronger one.", 400

    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    # Search for the pattern in the text
    match = re.search(pattern, email)
    if not match:
        return "Invalid email format.", 400

    return("password is valid."), 200
