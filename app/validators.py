import re

def validate_email_address(email: str) -> bool:
    """
    Validates an email address using a regular expression.
    
    Args:
        email (str): The email address to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def validate_password(password: str) -> bool:
    """
    Validates a password for minimum security requirements.
    
    Requirements:
        - At least 8 characters long.
        - Contains at least one uppercase letter.
        - Contains at least one lowercase letter.
        - Contains at least one number.
        - Contains at least one special character.
    
    Args:
        password (str): The password to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.match(password_regex, password) is not None
