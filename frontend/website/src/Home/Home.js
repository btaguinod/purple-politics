import React, { Component } from 'react'
import Cards from './Cards/Cards'
import Headlines from './Headlines/Headlines'
import './Home.css'

import config from '../config'

export default class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {
            cardEvents: [],
            headlineEvents: [],
            isLoaded: false
        }
    }

    componentDidMount() {
        fetch(config.backendUrl + '/home-events')
            .then(response => response.json())
            .then(data => {
                // let cardEvents = data['cardEvents'];

                
                // cardEvents = cardEvents.filter(cardEvent => cardEvent.imageUrl !== '')
                // cardEvents.sort((a, b) => 
                //     b.companies.length - a.companies.length
                // );
                // cardEvents = cardEvents.slice(0, 30)

                // let headlineEvents = [...data];
                // headlineEvents.sort((a, b) => 
                //     new Date(b.latestTime) - new Date(a.latestTime)
                // );
                // headlineEvents = headlineEvents.slice(0, 7)
                this.setState({
                    cardEvents: data['cardEvents'],
                    headlineEvents: data['headlineEvents'],
                    isLoaded: true
                });
            })
    }

    render() {
        if (!this.state.isLoaded)
            return <div />
        
        return (
            <div id="home">
                <Cards events={this.state.cardEvents}/>
                <Headlines events={this.state.headlineEvents}/>
            </div>
        )
    }
}
