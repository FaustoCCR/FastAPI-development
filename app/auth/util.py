from passlib.context import CryptContext

"""
Create a PassLib "context". This is what will be used to hash and verify password
It also has the functionality to use different hashing algorithms, including
deprecated old ones.
"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    # TODO: Check generated warning message to python 3.11 version
    """Hash a password coming from the user

    Args:
        password (str): user password

    Returns:
        str: password hash
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if a received password matches the hash stored

    Args:
        plain_password (str): plain password
        hashed_password (str): hashed password stored

    Returns:
        bool: comparison result
    """
    return pwd_context.verify(plain_password, hashed_password)
