from model import Recipe,PydanticObjectId, Ingredient, User
#MongoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://meggan567:lm5d9889@cluster0.lpghgsq.mongodb.net/')
database = client.RecipeGenerator
collectionR = database.Recipes
collectionU = database.Users

#Recipe:
async def fetch_recipe(id):
    id = PydanticObjectId(id)
    document = await collectionR.find_one({"_id": id}) 
    recipe = Recipe(**document)
    recipe.id = str(document.get("_id"))
    return recipe

async def fetch_recipes():
    recipes = []
    cursor = collectionR.find({}) 
    async for document in cursor: 
        recipe = Recipe(**document)
        recipe.id = str(document.get("_id"))
        recipes.append(recipe) 
    return recipes

async def create_recipe(recipe):
    document = recipe
    result = await collectionR.insert_one(document)
    return document

async def update_recipe(id, title, ingredients):
    id = PydanticObjectId(id)
    ings = [{"name":x.name, "quantity":x.quantity} for x in ingredients]
    await collectionR.update_one({"_id":id},{"$set":{"title": title, 
        "ingredients": ings}}) 
    document = await collectionR.find_one({"_id":id}) 
    recipe = Recipe(**document)
    recipe.id = str(document.get("_id"))
    return recipe
 
async def remove_recipe(id):
    await collectionR.delete_one({"_id":PydanticObjectId(id)})
    return True

#User:
async def add_ingredient(id, ingredient: Ingredient):
    id = PydanticObjectId(id)
    db_user = await collectionU.find_one({"_id":id}) #stored as dictionary from db
    user = User(**db_user) #stored as User
    user.ingredients.append(ingredient)
    ings = [{"name":x.name, "quantity":x.quantity} for x in user.ingredients]
    await collectionU.update_one({"_id":id},{"$set":{ 
        "ingredients": ings}}) 
    return user

async def delete_ingredient(user_id, name):
    user_id = PydanticObjectId(user_id)
    db_user = await collectionU.find_one({"_id":user_id}) 
    if db_user is not None:
        user = User(**db_user) 
        for x in user.ingredients:
            if x.name == name:
                user.ingredients.remove(x)
                break
        ings = [{"name":x.name, "quantity":x.quantity} for x in user.ingredients]
        await collectionU.update_one({"_id":user_id},{"$set":{ 
        "ingredients": ings}}) 
        return user
    else:
        return None

async def create_user(user):
    result = await collectionU.insert_one(user)
    return user

async def fetch_user(id):
    id = PydanticObjectId(id)
    db_user = await collectionU.find_one({"_id": id}) 
    if db_user is not None:
        user = User(**db_user)
        #user._id = str(db_user.get("_id"))
        return user
    else:
        return None