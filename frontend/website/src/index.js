import React from 'react';
import ReactDOM from 'react-dom';
import Header from './Header/Header';
import Home from './Home/Home';
import About from './About/About';
import './index.css'

import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

ReactDOM.render(
  <React.StrictMode>
    <Router >
      <Header />
      <Switch>
        <Route path="/about"> <About /> </Route>
        <Route path="/"> <Home /> </Route>
      </Switch>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);
