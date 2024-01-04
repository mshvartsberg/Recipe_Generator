import './App.css';
import React, {useState, useEffect} from 'react';
import IngredientCard from './components/IngredientCard';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  const [ingredientList, setIngredientList] = useState([{}]); 
  const [name, setName] = useState('');
  const [quantity, setQuantity] = useState(0);
  const [refreshCount, setRefreshCount] = useState(0);
  const id = '6594d98b606a2e3354ff81cc';

  // read/update user's ingredients:
  useEffect(() => {
    axios.get(`http://localhost:8000/api/user/${id}`) 
      .then(res => { 
        console.log(res.data);
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
  }; //how does this call add_user_ingredient? and should it be put cuz im editting the user?

  return (
    <div className="App">
      <h1>User Name_______User Email</h1>
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
          id={id} ingredient={ingredient} ingredientList={ingredientList} 
          refresher={setRefreshCount}/>))}
        </div>
      </div>
    </div>
  );
}

export default App;
