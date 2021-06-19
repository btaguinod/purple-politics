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
                        <a class="page-link" href="#home">
                            Home
                        </a>
                        <a class="page-link" href="#about">
                            About
                        </a>
                    </div>
                </div>
            </header>
        )
    }
}
