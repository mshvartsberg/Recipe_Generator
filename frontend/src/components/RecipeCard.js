import React from 'react'
import IngredientCard from './IngredientCard';

function RecipeCard({id, recipe, refresher}){
    return(
        <div className = "card recipe">
            <div className = "card-body">
                <h3>{recipe.title}</h3>
                <h6>Ingredients:</h6>
                <div>
                    {recipe.ingredients.map((ingredient) => (<IngredientCard 
                    showDelete={false} id={id} ingredient={ingredient} ingredientList={recipe.ingredients} 
                    refresher={refresher}/>))}
                </div>
            </div>
        </div>
    )
}
export default RecipeCard;