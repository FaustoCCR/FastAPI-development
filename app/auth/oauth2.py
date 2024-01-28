from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

"""
* OAuth2PasswordBearer
It represents the OAuth2 password bearer authentication scheme.
tokenUrl: it is a parameter that specifies the URL where the client
can request a token. This URL is typically used by the client to obtain
an access token by providing their username and password.
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# * SECRET KEY
# * ALGORITHM
# * EXPIRATION TIME

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
):
    """Create a session access token

    Args:
        data (dict): token payload
        expires_delta (Optional[timedelta], optional): Token expiration time in minutes. Defaults to None.

    Returns:
        str: encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(
    token: str, credentials_exception: Exception
) -> schemas.TokenData:
    """
    Verify the access token and return the corresponding token data.

    Args:
        token (str): The access token to be verified.
        credentials_exception (Exception): The exception to be raised if the token is invalid.

    Raises:
        credentials_exception (Exception): Raised when the token is invalid.

    Returns:
        schemas.TokenData: The token data extracted from the access token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)
