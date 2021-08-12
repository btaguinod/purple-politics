import React, { Component } from 'react';
import './Header.css';
import { Link } from "react-router-dom";
import MobileButton from './MobileButton/MobileButton';
import SearchBar from './SearchBar/SearchBar';

export default class Header extends Component {
    render() {
        return (
            <header>
                <div id="inner-header-container">
                    <Link id="logo" to="/">
                        <span id="purple">PURPLE</span> POLITICS
                    </Link>
                    <SearchBar className="mobile" />
                    <MobileButton />
                    <div className="page-links">
                        <SearchBar className="" />
                        <Link className="page-link" to="/">Home</Link>
                        <Link className="page-link" to="/events">Events</Link>
                        <Link className="page-link" to="/about">About</Link>
                    </div>
                </div>
            </header>
        );
    }
}
