import React, { Component } from 'react'
import Card from './Card'
import './Cards.css'

export default class Cards extends Component {
    constructor(props) {
        super(props);
        let groupSizes = [3, 2, 3]

        let eventsLength = props.events.length;

        let lastGroupSize = eventsLength;
        for (let size of groupSizes)
            lastGroupSize -= size;

        groupSizes = groupSizes.concat([lastGroupSize]);

        let cardTypes = [
            'lg',
            'sm',
            'sm',
            'md-1', 
            'md-2',
            'sm',
            'lg'
        ];

        let extraCardTypes = [];
        for (let i = 0; i <= lastGroupSize; i++) {
            extraCardTypes.push('sm')
        }
        cardTypes = cardTypes.concat(extraCardTypes)
        
        this.cardTypes = cardTypes
        this.groupSizes = groupSizes
    }

    render() {
        let cards = this.props.events.map((event, i) => 
            <Card 
                key={event.eventId} 
                event={event} 
                type={this.cardTypes[i]}
            />
        )

        let i = 0;
        let groups = this.groupSizes.map((size, groupNum) => {
            let group = [];
            for (let j = 0; j < size; j++) {
                group.push(cards[i]);
                i++;
            }
            let className = 'card-group-' + String(groupNum + 1);
            return (
                <div key={groupNum} className={className}>{group}</div>
            )
        })

        return (
            <div id="cards">
                <div id="cards-heading">Most Covered Events</div>
                {groups}
            </div>
        )
    }
}
