import React, { Component } from 'react'
import Cards from './Cards/Cards'
import Headlines from './Headlines/Headlines'
import './Home.css'
// import getArticles from './mock_article_sets/articles'
import getArticles from './mock_article_sets/rss'

export default class Home extends Component {
    constructor(props) {
        super(props);
        this.events = getArticles(50);
    }

    render() {
        return (
            <div id="home">
                <Cards events={this.events.slice(7)}/>
                <Headlines events={this.events.slice(0, 7)}/>
            </div>
        )
    }
}