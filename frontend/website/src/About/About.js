import React from 'react'
import './About.css'

export default function About() {
    return (
        <div id="about">
            <div className="about-title"> Purpose </div>
            <div className="about-description">
                <span className="bold purple">Purple Politics</span> is a website designed to help you understand all perspectives on recent political events. 
                <br /><br />
                The complexity of political topics is too great to describe their ethics with a single label. They cannot be boiled down to just <span className="blue">blue</span> or <span className="red">red</span>. 
                <br /><br />
                Rather, they are <span className="bold purple">purple</span>. Their ethics are a mix of political sides. 
                <br /><br />
                By giving you <span className="bold">media source biases</span> (provided by AllSides), <span className="bold">text emotion</span>, and <span className="bold">text sentiment</span>, this website gives you a deeper view into the ethical complexity of an article. 
                <br /><br />
                This allows you to decide for yourself where your beliefs stand, allowing you to form an option that aligns with your beliefs rather than the beliefs of singular sources.
            </div>
        </div>
    )
}

