from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import Recipe, RecipeDB
from model import User
from model import Ingredient
from typing import List

#App object
app = FastAPI()
from database import (
    fetch_recipe,
    fetch_recipes,
    create_recipe,
    update_recipe,
    remove_recipe,
    add_ingredient,
    create_user,
    fetch_user,
    delete_ingredient,
)
origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Recipe API Calls:
@app.get("/api/recipe")
async def get_recipes(): 
    response = await fetch_recipes() 
    print(response)
    return response
@app.get("/api/recipe{id}", response_model=Recipe)
async def get_recipe_by_id(id):
    response = await fetch_recipe(id)
    if response:
        return response
    raise HTTPException(404, f"there is no todo item with this id {id}") 
# returns all recipes that a user can cook based on a certain threshold
# add so that it can tell the user which ingredients are missing and need to be bought
@app.get("/api/recipes_to_cook/{user_id}")
async def get_recipes_to_cook(user_id, threshold: float): 
    #threshold represents a percent of ingredients that must match (.50 = 50%)
    all_recipes = await fetch_recipes()
    cook_recipes: List[Recipe] = []
    user = await get_user_by_id(user_id)
    for recipe in all_recipes:
        count = 0
        total_ingredients = len(recipe.ingredients)
        for ingredient in recipe.ingredients:
            for ing in user.ingredients:
                if (ingredient.name == ing.name):
                    count+=1
        if (count/total_ingredients >= threshold):
            cook_recipes.append(recipe)
        for ingredient in recipe.ingredients:
            buyFlag = False
            for ing in user.ingredients:
                if (ing.name == ingredient.name):
                    buyFlag = True
                    break
            if (buyFlag == False):
                recipe.buyIngredients.append(ingredient)
            else:
                buyFlag = False
    return cook_recipes
@app.post("/api/recipe", response_model=RecipeDB)
async def post_recipe(recipe: RecipeDB):
    response = await create_recipe(recipe.model_dump()) 
    if response:
        return response
    raise HTTPException(400, "Something went wrong") 

@app.put("/api/recipe/{id}", response_model=Recipe)
async def put_recipe(id, recipe: RecipeDB):
    response = await update_recipe(id,recipe.title,recipe.ingredients)
    if response:
        return response
    raise HTTPException(404, f"there is no todo item with this id {id}") 

@app.delete("/api/recipe/{id}")
async def delete_recipe(id):
    response = await remove_recipe(id)
    if response:
        return "Successfully deleted the recipe!"
    raise HTTPException(404, f"there is no recipe with this id {id}") 

#User API Calls:
@app.post("/api/user", response_model=User)
async def post_user(user: User):
    response = await create_user(user.model_dump()) 
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@app.put("/api/add_user_ingredient/{id}", response_model=User)
async def add_user_ingredient(id, ingredient: Ingredient):
    response = await add_ingredient(id,ingredient)
    if response:
        return response
    raise HTTPException(404, f"there is no user with this id {id}") 

@app.put("/api/delete_user_ingredient/{id}", response_model=User)
async def delete_user_ingredient(id, name):
    response = await delete_ingredient(id, name)
    if response:
        return response
    raise HTTPException(404, f"there is no user with this id {id}") 

@app.get("/api/user/{id}", response_model=User)
async def get_user_by_id(id):
    response = await fetch_user(id)
    if response:
        return response
    raise HTTPException(404, f"there is no user item with this id {id}") 
