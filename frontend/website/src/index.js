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
    <Header />
    <Home />
  </React.StrictMode>,
  document.getElementById('root')
);
