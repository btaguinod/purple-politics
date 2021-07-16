import React, { Component } from 'react'
import './Headlines.css'

export default class Headlines extends Component {
    render() {
        return (
            <div id="headlines">
                <div id="headlines-label">Top Headlines</div>
                {this.props.events.map(event => 
                    <div className="headline-title">{event.title}</div>
                )}
            </div>
        )
    }
}
