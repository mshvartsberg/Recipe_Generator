from model import Recipe,PydanticObjectId, Ingredient
#MongoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://meggan567:lm5d9889@cluster0.lpghgsq.mongodb.net/')
database = client.RecipeGenerator
collectionR = database.Recipes

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