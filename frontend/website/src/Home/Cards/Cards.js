import React, { Component } from 'react'
import Card from './Card'
import './Cards.css'

export default class Cards extends Component {
    constructor(props) {
        super(props);
        this.state = {
            cardTypes: [
                'lg',
                'sm',
                'sm',
                'md-1', 
                'md-2',
                'sm',
                'lg'
            ],
            groupSizes: [3, 2, 3],
            isLoaded: false
        }
    }

    componentDidUpdate(prevProps) {
        if (this.props.events.length !== prevProps.events.length) {
            this.setState((state, props) => {
                let eventsLength = props.events.length;

                let lastGroupSize = eventsLength;
                for (let size of state.groupSizes)
                    lastGroupSize -= size;

                let groupSizes = state.groupSizes.concat([lastGroupSize]);

                let extraCardTypes = [];
                for (let i = 0; i <= lastGroupSize; i++) {
                    extraCardTypes.push('sm')
                }
                let cardTypes = state.cardTypes.concat(extraCardTypes)

                return { groupSizes, cardTypes, isLoaded: true }
            })
        }
    }

    render() {
        if (!this.state.isLoaded)
            return <span />
        
        let cards = this.props.events.map((event, i) => 
            <Card 
                key={event.eventId} 
                event={event} 
                type={this.state.cardTypes[i]}
            />
        )

        let i = 0;
        let groups = this.state.groupSizes.map((size, groupNum) => {
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
