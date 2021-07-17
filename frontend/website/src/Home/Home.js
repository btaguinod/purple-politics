import React, { Component } from 'react'
import Cards from './Cards/Cards'
import Headlines from './Headlines/Headlines'
import './Home.css'
import getArticles from './mock_article_sets/rss'

export default class Home extends Component {
    constructor(props) {
        super(props);
        this.events = getArticles(50);
        this.state = {
            error: null,
            isLoaded: false,
            cardEvents: [],
            headlineEvents: []
        }
    }

    componentDidMount() {
        fetch('https://purple-politics.herokuapp.com/events')
            .then(response => response.json())
            .then(data => {
                let cardEvents = [...data];
                cardEvents = cardEvents.filter(cardEvent => cardEvent.imageUrl !== '')
                cardEvents.sort((a, b) => 
                    b.companies.length - a.companies.length
                );
                cardEvents = cardEvents.slice(0, 30)

                let headlineEvents = [...data];
                headlineEvents.sort((a, b) => 
                    b.latestTime - a.latestTime
                );
                headlineEvents = headlineEvents.slice(0, 7)
                this.setState({
                    cardEvents,
                    headlineEvents
                });
            })
    }

    render() {
        return (
            <div id="home">
                <Cards events={this.state.cardEvents}/>
                <Headlines events={this.state.headlineEvents}/>
            </div>
        )
    }
}
