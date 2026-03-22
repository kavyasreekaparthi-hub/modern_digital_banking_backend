from passlib.context import CryptContext

# Set up the hashing context using bcrypt
# This creates a cryptographically secure wrapper for password management
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hashes a password using bcrypt. 
    Truncates to 72 characters because bcrypt natively ignores 
    any input beyond the 72-byte limit.
    """
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a stored hash.
    Truncates input to 72 characters to match the hashing logic.
    """
    return pwd_context.verify(plain_password[:72], hashed_password)