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
                    <div id="button-mobile">
                        <input type="checkbox" id="button-checkbox-mobile" />
                        <div id="page-links-mobile">
                        <Link className="page-link-mobile" to="/"> Home </Link>
                        <Link className="page-link-mobile" to="/about"> About </Link>
                        </div>
                        <span />
                        <span />
                        <span />
                    </div>
                    <div id="page-links">
                        <Link className="page-link" to="/"> Home </Link>
                        <Link className="page-link" to="/about"> About </Link>
                    </div>
                </div>
            </header>
        )
    }
}
