import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import './Headlines.css'

export default class Headlines extends Component {
    render() {
        return (
            <div id="headlines">
                <div id="headlines-label">Top Headlines</div>
                {this.props.events.map(event => 
                    <Link 
                        className="headline-title"
                        to={"articles/" + event.eventId}>
                        {event.title}
                    </Link>
                )}
            </div>
        )
    }
}
