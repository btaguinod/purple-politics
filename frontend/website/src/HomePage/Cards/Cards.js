import React, { Component } from 'react'
import Card from './Card'
import './Cards.css'

export default class Cards extends Component {
    constructor(props) {
        super(props);
        this.cardTypes = [
            "card-medium-1", 
            "card-medium-2",
            "card-large",
            "card-small",
            "card-small",
            "card-small",
            "card-large"
        ];
        while (this.cardTypes.length < this.props.articles.length)
            this.cardTypes.push("card-small");
        
    }
    render() {
        return (
            <div id="cards">
                {this.props.articles.map((article, i) => 
                    <Card article={article} className={this.cardTypes[i]}/>
                )}
            </div>
        )
    }
}
