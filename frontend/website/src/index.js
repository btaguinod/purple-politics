import React from 'react';
import ReactDOM from 'react-dom';
import Header from './Header/Header';
import HomePageArticles from './HomePage/HomePageArticles';
import './index.css'

ReactDOM.render(
  <React.StrictMode>
    <Header />
    <HomePageArticles/>
  </React.StrictMode>,
  document.getElementById('root')
);
