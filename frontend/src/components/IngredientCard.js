import axios from 'axios'
import React from 'react'

function IngredientCard({showDelete, id, ingredient, refresher}){
    const deleteIngredient = (name) => {
        axios.put(`http://localhost:8000/api/delete_user_ingredient/${id}?name=${name}`)
        .then(res => {
            console.log(res.data)
            refresher (Math.random());
        })}
        return(
            <div className = "card ingredient">
                <div className = "card-body">
                    <h4>{ingredient.name}</h4>
                    <h6>Amount: {ingredient.quantity} units</h6>
                    {showDelete &&
                    <button onClick={() => 
                        deleteIngredient(ingredient.name)} style ={{ marginLeft: '10px'}}>
                        <img
                            src={require("./download.png")}
                            style={{width: '20px', height: '20px' }} 
                        />
                    </button>}
                </div>
            </div>
        )
    }
    export default IngredientCard;