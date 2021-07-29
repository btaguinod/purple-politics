import React, { Component } from 'react'
import './Header.css'
import { Link } from "react-router-dom";

export default class Header extends Component {
    render() {
        return (
            <header>
                <div id="inner-header-container">
                    <Link id="logo" to="/">
                        <span id="purple">PURPLE</span> POLITICS
                    </Link>
                    <div id="button">
                        <input type="checkbox" id="button-checkbox" className="mobile" />
                        <div className="page-links mobile">
                            <Link className="page-link" to="/">Home</Link>
                            <Link className="page-link" to="/events">Events</Link>
                            <Link className="page-link" to="/about">About</Link>
                        </div>
                        <span />
                        <span />
                        <span />
                    </div>
                    <div className="page-links">
                        <Link className="page-link" to="/">Home</Link>
                        <Link className="page-link" to="/events">Events</Link>
                        <Link className="page-link" to="/about">About</Link>
                    </div>
                </div>
            </header>
        )
    }
}
