import './App.css';
import React, {useState, useEffect} from 'react';
import IngredientCard from './components/IngredientCard';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import RecipeCard from './components/RecipeCard';
import navValues from './navValues';

function App() {
  const [ingredientList, setIngredientList] = useState([{}]); 
  const [recipeList, setRecipeList] = useState([]); 
  const [name, setName] = useState('');
  const [quantity, setQuantity] = useState(0);
  const [refreshCount, setRefreshCount] = useState(0);
  const [currentUser, setCurrentUser] =useState({});
  const [currentPage, setCurrentPage] =useState(navValues.ingredients); //change default to welcome once it's made
  const id = '6594d98b606a2e3354ff81cc';
  const threshold = 0.5;

  // read/update user's ingredients:
  useEffect(() => {
    axios.get(`http://localhost:8000/api/user/${id}`) 
      .then(res => { 
        console.log(res.data);
        setCurrentUser(res.data);
        setIngredientList(res.data.ingredients)
      })//.catch to give an error
  }, [refreshCount]); 

  //post an ingredient (edit/put user)
  const addIngredientHandler = () => {
    axios.put(`http://localhost:8000/api/add_user_ingredient/${id}`, {'name': name, 'quantity':quantity})
    .then(res => {
      console.log(res);
      setRefreshCount(refreshCount + 1);
    })
  }; 

  const getRecipeHandler = () => {
    setCurrentPage(navValues.recipesToCook);
    axios.get(`http://localhost:8000/api/recipes_to_cook/${id}?threshold=${threshold}`)
    .then(res => {
      console.log(res.data);
      setRecipeList(res.data)
      setRefreshCount(refreshCount + 1);
    })
  };
  const btiHandler = () => {
    setCurrentPage(navValues.ingredients);
  }

  if (currentPage == navValues.ingredients){
    return(
    //--------------------------------------ingredients component
    <div className="App">
      <h1>{currentUser.name}        {currentUser.email} </h1>
      <div className="card-body">
        <h3 className="card text-white bg-dark mb-3">Add an ingredient:</h3>
        <span className="card-text"> 
          <input className="mb-2 form-control nameIn" 
          onChange={event => setName(event.target.value)} placeholder='name'/>
          <input className="mb-2 form-control quantityIn" 
          onChange={event => setQuantity(event.target.value)} placeholder='quantity'/>
          <button className="btn btn-outline-primary mx-2 mb-3" 
          style={{'borderRadius':'50px','font-weight':'bold'}} onClick={addIngredientHandler}>Add Ingredient</button>
        </span>
        <h5 className="card text-white bg-dark mb-3">Your Ingredients:</h5>
        <div>
          {ingredientList.map((ingredient) => (<IngredientCard 
          showDelete={true} id={id} ingredient={ingredient} refresher={setRefreshCount}/>))}
        </div>
          <button onClick={getRecipeHandler}>Get Recipes!</button> </div> 
      </div>
    );}
    else if (currentPage == navValues.recipesToCook){
      return(
  //----------------------------------------------------------------------- 
        <div className="App">
          <div>
              {recipeList.map((recipe) => (<RecipeCard 
              id={id} recipe={recipe} refresher={setRefreshCount}/>))}
          </div>
          <button onClick={btiHandler}>Back to Ingredients</button>
        </div>);
    }    
  
}

export default App;
