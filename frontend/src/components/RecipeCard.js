import React from 'react'
import IngredientCard from './IngredientCard';

function RecipeCard({id, recipe, refresher, showBuy}){
    return(
        <div className = "card recipe">
            <div className = "card-body">
                <h2>{recipe.title}</h2>
                <h3>Ingredients:</h3>
                <div>
                    {recipe.ingredients.map((ingredient) => (<IngredientCard 
                    showDelete={false} id={id} ingredient={ingredient} ingredientList={recipe.ingredients} 
                    refresher={refresher}/>))}
                </div>
                {showBuy &&
                <div>
                <h4>Buy the following ingredients:</h4>
                    {recipe.buyIngredients.map((ingredient) => (<IngredientCard 
                    showDelete={false} id={id} ingredient={ingredient} ingredientList={recipe.buyIngredients} 
                    refresher={refresher}/>))}
                </div>}
            </div>
        </div>
    )
}
export default RecipeCard;