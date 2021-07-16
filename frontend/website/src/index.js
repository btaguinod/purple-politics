import React from 'react';
import ReactDOM from 'react-dom';
import Header from './Header/Header';
import Home from './Home/Home';
import './index.css'

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

ReactDOM.render(
  <React.StrictMode>
    <Router >
      <Header />
      <Switch>
        <Route path="/" component={Home} />
      </Switch>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);
