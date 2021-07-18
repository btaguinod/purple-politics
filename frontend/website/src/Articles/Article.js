import React from 'react'
import './Articles.css'

export default function Article(props) {
    const biases = {'-1': 'L', '-0.5': 'CL', '0': 'C', '0.5': 'CR', '1': 'R'}
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    const formatDate = date => {
        return months[date.getMonth()] + ' ' + date.getDate() + ', ' + 
            date.getFullYear();
    }
    const capitalize = text => 
        (text[0].toUpperCase() + text.slice(1, text.length))
    const getSentimentClass = () => {
        let sentiment = props.article.textInfo.sentiment;
        let className = 'article-sentiment ';
        if (sentiment > 0) 
            className += 'positive'
        else if (sentiment < 0)
            className += 'negative'
        return className
    }
    const getEmotionClass = () => {
        let sentiment = props.article.textInfo.emotion;
        let className = 'article-sentiment ';
        className += sentiment === 'joy' ? 'positive' : 'negative'
        return className
    }


    let image = <span />;
    if (props.article.imageUrl !== "")
        image = <div className="article-image">
                    <img
                        src={props.article.imageUrl} 
                        alt="news"
                    />
                </div>

    let bias = biases[props.article.company.bias.toString()]
    return (
        <a href={props.article.articleUrl} className="article">
            <div className="left-container">
                <div className="image-title-container">
                    {image}
                    <div className="article-title">
                        {props.article.title}
                    </div>
                </div>
                <div className="article-description">
                    {props.article.description}
                </div>
                <div className="company-date-container">
                    <span className="article-company">
                        {props.article.company.name + ' '}
                    </span>
                    <span className={"article-bias " + bias.toLowerCase()}>
                        {bias}
                    </span>
                    {' | '}
                    <span className="article-date">
                        {formatDate(new Date(props.article.publishedTime))}
                    </span>
                </div>
            </div>
            <div className="right-container">
                <div className="sentiment-container">
                    Sentiment:
                    <div className={getSentimentClass()}>
                        {Math.round(props.article.textInfo.sentiment*100)}%
                    </div>
                </div>
                
                <div className="emotion-container">
                    Emotion:
                    <div className={getEmotionClass()}>
                        {capitalize(props.article.textInfo.emotion)}
                    </div>
                </div>
            </div>
        </a>
    )
}
