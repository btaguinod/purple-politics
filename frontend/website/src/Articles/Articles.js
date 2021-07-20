import { useEffect, useState } from 'react'
import Article from './Article'
import './Articles.css'
import { nanoid } from 'nanoid'

export default function Articles(props) {

    const [articles, setArticles] = useState();
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        let eventId = props.match.params.eventId
        fetch('https://purple-politics.herokuapp.com/articles/' + eventId)
            .then(response => response.json())
            .then(data => {
                for (let article of data) {
                    article['articleId'] = nanoid();
                }
                setArticles(data);
                setIsLoaded(true);
            })
    }, [props.match.params.eventId])

    if (!isLoaded)
        return <div />

    return (
        <div id="articles-container">
            <div id="articles">
                <div id="heading">Event Articles</div>
                {articles.map(article => 
                    <Article key={article.articleId} article={article} />
                )}
            </div>
        </div>
    )
}
