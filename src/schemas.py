from pydantic import BaseModel

class Users(BaseModel):
    name:str
    email:str
    phone:str
    password:str
    occupation:str

class Admin(BaseModel):
    name:str
    email:str
    password:str

class Login(BaseModel):
    email:str
    password:str