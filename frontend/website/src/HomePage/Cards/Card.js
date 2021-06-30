import React, { Component } from 'react'

export default class Card extends Component {
    render() {
        return (
            <div className={"card-base-" + this.props.type}>
                {/* <img
                    className={"card-image-" + this.props.type}
                    src={this.props.article.image} 
                    alt="news"
                /> */}
                <div className={"card-image-" + this.props.type}>
                    <img
                        src={this.props.article.image} 
                        alt="news"
                    />
                </div>
                <div className={"card-text-" + this.props.type}>
                    <div className={"card-title-" + this.props.type}>
                        {this.props.article.title}
                    </div>
                    <div className={"card-date-" + this.props.type}>
                        {this.props.article.date}
                    </div>
                    <div className={"card-sources-" + this.props.type}>
                        {this.props.article.sources.join(" | ")}
                    </div>
                </div>
            </div>
        )
    }
}
