import React from 'react';
import './MobileButton.css';
import { Link } from "react-router-dom";

export default function MobileButton() {
    return (
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
    );
}
