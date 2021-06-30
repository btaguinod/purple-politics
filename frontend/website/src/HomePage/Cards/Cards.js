import React, { Component } from 'react'
import Card from './Card'
import './Cards.css'

export default class Cards extends Component {
    constructor(props) {
        super(props);
        this.cardTypes = [
            "md-1", 
            "md-2",
            "lg",
            "sm",
            "sm",
            "sm",
            "lg"
        ];
        while (this.cardTypes.length < this.props.articles.length)
            this.cardTypes.push("sm");
    }
    render() {
        return (
            <div id="cards">
                {this.props.articles.map((article, i) => 
                    <Card article={article} type={this.cardTypes[i]}/>
                )}
            </div>
        )
    }
}
