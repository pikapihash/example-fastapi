from passlib.context import CryptContext
#tell the machine that what is the algorithm we use to encrypt the password
#btw we use bcrypt algorithm 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password , hashed_password):
    return pwd_context.verify(plain_password,hashed_password)