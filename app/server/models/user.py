from typing import Optional

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    full_name: str = Field(...)
    user_name: str = Field(...)
    password: str = Field(...)
    address: str = Field(...)
    avatar: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "full_name": "Nguyen Van A",
                "user_name": "avannguyen",
                "password": "123",
                "address": "Can Tho",
                "avatar": "https://avatar.com.vn"
            }
        }

class UpdateUserModel(BaseModel):
    full_name: Optional[str]
    user_name: str
    password: Optional[str]
    address: Optional[str]
    avatar: Optional[str]
    
    class Config:
        schema_extra = {
            "example": {
                "full_name": "Nguyen Van A",
                "user_name": "avannguyen",
                "password": "123",
                "address": "Can Tho",
                "avatar": "https://avatar.com.vn"
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message,
    }