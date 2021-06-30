import React, { Component } from 'react'
import Cards from './Cards/Cards'
import Headlines from './Headlines/Headlines'
import './HomePageArticles.css'
import getArticles from './mock_article_sets/articles'

export default class HomePageArticles extends Component {
    constructor(props) {
        super(props);
        this.articles = getArticles(50);
    }

    render() {
        return (
            <div id="home-page-articles">
                <Cards articles={this.articles.slice(7)}/>
                <Headlines articles={this.articles.slice(0, 7)}/>
            </div>
        )
    }
}