from typing import List, Optional

from pydantic import BaseModel, Field


class ArticleSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    author: str = Field(...)
    comment: int = Field(...)
    image: str = Field(...)
    keywords: List = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Learning python with Fu",
                "content": "blah blah blah...!",
                "author": "Phu Nguyen",
                "comment": 200,
                "image": "https://img.com.vn",
                "keywords":['a','b','c']
            }
        }

class UpdateArticleModel(BaseModel):
    title: Optional[str]
    content: Optional[str]
    author: Optional[str]
    comment: Optional[int]
    image: Optional[str]
    keywords: List[str]
    

    class Config:
        schema_extra = {
            "example": {
                "title": "Learning python with Fuk",
                "content": "blah blah blah...!",
                "author": "Phu Gia Nguyen",
                "comment": 201,
                "image": "https://img113.com.vn",
                "keywords":['a','b','c']
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