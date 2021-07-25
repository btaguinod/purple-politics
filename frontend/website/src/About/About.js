import React from 'react'
import './About.css'

export default function About() {
    return (
        <div id="about">
            <div className="about-title"> Purpose </div>
            <div className="about-description">
                <span className="bold purple">Purple Politics</span> is a website designed to help you understand all perspectives on recent political events. 
                <br /><br />
                Political events in the US are usually marked as positive for <span className="blue">Democrats</span> or <span className="red">Republicans</span>. However, these events are too complex to be labeled as one side or the other. The ethics behind each story cannot be boiled down to just <span className="blue">blue</span> or <span className="red">red</span>.
                <br /><br />
                Rather, they are <span className="bold purple">purple</span>. A mix of both political sides. 
                <br /><br />
                By giving you <span className="bold">media biases</span>, <span className="bold">text emotion</span>, and <span className="bold">text sentiment</span>, this website gives you a deeper view into the ethical complexity of an article. 
                <br /><br />
                This allows you to decide for yourself where your beliefs stand, allowing you to form an option that aligns with your beliefs rather than the beliefs of singular sources.
            </div>
            <div className="about-title"> Media Biases </div>
            <div className="about-description split">
                <div>
                    Media Biases are the political sides news sources tend to lean towards. Showing these biases allow you to understand what viewpoints from different sides look like. The Media Bias Ratings on this site are provided by <a href="https://www.allsides.com/media-bias/media-bias-ratings">AllSides</a>.
                </div>
                <div>
                    <span className="article-bias l">L</span> = Left
                    <br /><br />
                    <span className="article-bias cl">CL</span> = Center Left
                    <br /><br />
                    <span className="article-bias c">C</span> = Center
                    <br /><br />
                    <span className="article-bias cr">CR</span> = Center Right
                    <br /><br />
                    <span className="article-bias r">R</span> = Right
                    <br /><br />
                </div>
            </div>
            <div className="about-title"> Text Emotion and Sentiment </div>
            <div className="about-description">
                Text emotion and sentiment describes the tone of the text and its connotation. Combined with Media Bias Ratings, this allows you to understand how different political sides feel about the same event. The text emotion and sentiment presented on this website was calculated using <a href="https://www.ibm.com/cloud/watson-natural-language-understanding">IBM Watson Natural Language Understanding</a>.
            </div>
            <div className="about-title">Impartiality</div>
            <div className="about-description">
            <span className="bold purple">Purple Politics</span> is not advertising for or siding with any political party. This content is provided without bias towards any political side.
            </div>
            
        </div>
    )
}

