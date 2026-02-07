from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from jose import jwt,JWTError
import os
from RAG_APP.db import sessionLocal
