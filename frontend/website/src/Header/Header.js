import React, { Component } from 'react'
import './Header.css'
import { Link } from "react-router-dom";

export default class Header extends Component {
    render() {
        return (
            <header>
                <div id="inner-header-container">
                    <a id="logo" href="#home">
                        <span id="purple">PURPLE</span> POLITICS
                    </a>
                    <div id="page-links">
                        <Link className="page-link" to="/home"> Home </Link>
                        <Link className="page-link" to="/about"> About </Link>
                    </div>
                </div>
            </header>
        )
    }
}
