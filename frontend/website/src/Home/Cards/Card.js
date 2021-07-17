import React, { Component } from 'react'

export default class Card extends Component {
    static titleSizes = {100:'sm', 90:'md', 60:'lg', 45:'xl'}
    constructor(props) {
        super(props);
        let titleLength = this.props.event.title.length;
        let closestSize = Object.keys(Card.titleSizes).reduce((prev, curr) => 
            Math.abs(Number(curr) - titleLength) < Math.abs(Number(prev) - titleLength) ? curr : prev
        )
        this.titleClass = "card-title-" + this.props.type + ' title-' + String(Card.titleSizes[closestSize]);
    }

    static months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    formatDate = date => {
        return Card.months[date.getMonth()] + ' ' + date.getDate() + ', ' + 
            date.getFullYear();
    }

    render() {
        let earliestDate = new Date(this.props.event.earliestTime);
        let latestDate = new Date(this.props.event.latestTime);
        earliestDate = this.formatDate(earliestDate);
        latestDate = this.formatDate(latestDate);
        let dateRange = earliestDate;
        if (earliestDate !== latestDate)
            dateRange += ' - ' + latestDate
        return (
            <div className={"card-base-" + this.props.type}>
                <div className={"card-image-" + this.props.type}>
                    <img
                        src={this.props.event.imageUrl} 
                        alt="news"
                    />
                </div>
                <div className={"card-text-" + this.props.type}>
                    <div className={this.titleClass}>
                        {this.props.event.title}
                    </div>
                    <div>
                        <div className={"card-date-" + this.props.type}>
                            {dateRange}
                        </div>
                        <div className={"card-sources-" + this.props.type}>
                            {this.props.event.companies.join(" | ")}
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
