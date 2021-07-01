import React, { Component } from 'react'
import './Headlines.css'

export default class Headlines extends Component {
    render() {
        return (
            <div id="headlines">
                <div id="headlines-label">Top Headlines</div>
                {this.props.articles.map(article => 
                    <div className="headline-title">{article.title}</div>
                )}
            </div>
        )
    }
}
