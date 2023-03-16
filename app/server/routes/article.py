
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..database import (add_article, delete_article, insert_data_from_json,
                        retrieve_article, retrieve_articles, update_article)
from ..models.article import (ArticleSchema, ErrorResponseModel, ResponseModel,
                              UpdateArticleModel)

router = APIRouter()


@router.post("/", response_description="Article data added into database")
async def add_article_data(article: ArticleSchema = Body(...)):
    article = jsonable_encoder(article)
    new_article = await add_article(article)
    print(new_article)
    return ResponseModel(new_article, "Article added successfully!")


@router.get("/", response_description="Articles retrieved")
async def get_articles():
    articles = await retrieve_articles()
    if articles:
        return ResponseModel(articles, "Articles data retrieved successfully!")
    return ResponseModel(articles, "Empty list returned")


@router.get("/{id}", response_description="Article data retrieved")
async def get_article_data(id):
    article = await retrieve_article(id)
    if article:
        return ResponseModel(article, "Article data retrieved successfully!")
    return ErrorResponseModel("An error occurred.", 404, "article doesn't exist.")


@router.put("/{id}")
async def update_article_data(id: str, req: UpdateArticleModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_article = await update_article(id, req)
    if updated_article:
        return ResponseModel(
            "Article with ID: {} name update is successful".format(id),
            "Article name updated successfully!",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the article data.",
    )


@router.delete("/{id}", response_description="Article data deleted from the database")
async def delete_article_data(id: str):
    deleted_article = await delete_article(id)
    if deleted_article:
        return ResponseModel(
            "Article with ID: {} removed".format(id), "Article deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Article with id {0} doesn't exist".format(id)
    )