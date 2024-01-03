from typing import List
from pydantic import BaseModel, Field
from bson.objectid import ObjectId as BsonObjectId

class Ingredient(BaseModel):
    name: str
    quantity: float

class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)

class RecipeDB(BaseModel):
    title: str
    ingredients: List[Ingredient] = []

class Recipe(RecipeDB):
    id: str | None = None #= Field(default_factory=PydanticObjectId, alias="_id")


class User(BaseModel):
    name: str
    ingredients: List[Ingredient] = []


