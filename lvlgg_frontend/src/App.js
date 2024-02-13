import './App.css';

import React from 'react'
import Navbar from './Components/Navbar'
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import './App.css'
import Explore from './Components/Pages/Explore'
import SignUp from './Components/Pages/SignUp'
import About from './Components/Pages/About'
import Guides from './Components/Pages/Guides'
import SignIn from './Components/Pages/SignIn'


function App() {
  return (
    <>
    <Router>
      <Navbar />
      <Switch>
        <Route path='/' exact component={Explore} />
        <Route path='/signup' component={SignUp} />
        <Route path='/about' component={About} />
        <Route path='/guides' component={Guides} />
        <Route path='/signin' component={SignIn} />
      </Switch>
    </Router>
    </>
      
    
  );
}

export default App;
