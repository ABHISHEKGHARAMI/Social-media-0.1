# getting the utility file for the user
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# function for the user to password hash
def hash(password : str):
    return pwd_context.hash(password)