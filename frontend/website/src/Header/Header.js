import React, { Component } from 'react'
import './Header.css'

export default class Header extends Component {
    render() {
        return (
            <header>
                <div id="inner-header-container">
                    <a id="logo" href="#home">
                        <span id="purple">PURPLE</span> POLITICS
                    </a>
                    <div id="page-links">
                        <a className="page-link" href="#home">
                            Home
                        </a>
                        <a className="page-link" href="#about">
                            About
                        </a>
                    </div>
                </div>
            </header>
        )
    }
}
