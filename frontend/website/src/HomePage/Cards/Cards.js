import React, { Component } from 'react'
import Card from './Card'
import './Cards.css'

export default class Cards extends Component {
    constructor(props) {
        super(props);
        let articles = this.props.articles.length;
        this.cardTypes = [
            "lg",
            "sm",
            "sm",
            "md-1", 
            "md-2",
            "sm",
            "lg"
        ];
        this.groupSizes = [3, 2, 3]
        while (this.cardTypes.length < articles)
            this.cardTypes.push("sm");

        let lastGroupSize = articles;
        for (let size of this.groupSizes)
            lastGroupSize -= size;
        this.groupSizes.push(lastGroupSize);
    }
    render() {
        let cards = this.props.articles.map((article, i) => 
                    <Card article={article} type={this.cardTypes[i]}/>
        )
        let i = 0;
        let groups = this.groupSizes.map((size, groupNum) => {
                    let group = [];
                    for (let j = 0; j < size; j++) {
                        group.push(cards[i]);
                        i++;
                    }
                    let className = "card-group-" + String(groupNum + 1);
                    return <div className={className}>{group}</div>
        })
        return (
            <div id="cards">
                {groups}
            </div>
        )
    }
}
