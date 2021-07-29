import { Link } from 'react-router-dom'

const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

const formatDate = dateString => {
    let date = new Date(dateString)
    return months[date.getMonth()] + ' ' + date.getDate() + ', ' + 
        date.getFullYear();
}

export default function NewsEvent(props) {
    let imageUrl = props.newsEvent.imageUrl
    let image
    if (imageUrl)
        image = <img src={props.newsEvent.imageUrl} alt="Event" />

    let link = "articles/" + props.newsEvent.eventId; 
    return (
        <Link className="news-event-base" to={link}>
                {image}
            <div className="news-event-text">
                <div className="news-event-title">{props.newsEvent.title}</div>
                <div className="news-event-date">
                    {formatDate(props.newsEvent.latestTime)}
                </div>
                <div className="news-event-companies">
                    {props.newsEvent.companies.join(" | ")}
                </div>
            </div>
        </Link>
    )
}
