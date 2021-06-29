import React, { Component } from 'react'

import './HomePageArticles.css'
import get_articles from './mock_article_sets/articles'

export default class HomePageArticles extends Component {
    constructor(props) {
        super(props);
        this.articles = get_articles(50);
    }

    render() {
        return (
            <div id="home-page-articles">
                
            </div>
        )
    }
}