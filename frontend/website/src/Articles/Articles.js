import { useEffect, useState } from 'react'
import Article from './Article'
import Sidebar from '../Sidebar/Sidebar'
import './Articles.css'
import { nanoid } from 'nanoid'

import config from '../config'

const sortOptions = ['Date', 'Bias']
const sortParams = {
    'Date': 'time',
    'Bias': 'bias'
}
const orderOptions = ['Ascending', 'Descending']
const orderParams = {
    'Descending': 'false',
    'Ascending': 'true'
    
}

export default function Articles(props) {
    const [articles, setArticles] = useState();
    const [isLoaded, setIsLoaded] = useState(false);
    const [sort, setSort] = useState('Date')
    const [order, setOrder] = useState('Descending')

    useEffect(() => {
        let eventId = props.match.params.eventId
        let sortQuery = 'sort=' + sortParams[sort]
        let orderQuery = 'ascending=' + orderParams[order]
        let queries = '?' + sortQuery + '&' + orderQuery
        fetch(config.backendUrl + '/articles/' + eventId + queries)
            .then(response => response.json())
            .then(data => {
                let dataArticles = data['articles']
                for (let article of dataArticles) {
                    article['articleId'] = nanoid();
                }
                setArticles(dataArticles);
                setIsLoaded(true);
            })
    }, [order, sort, props.match.params.eventId])

    if (!isLoaded)
        return <div />

    return (
        <div id="articles-container">
            <Sidebar
                sort={sort}
                sortOptions={sortOptions}
                setSort={setSort}
                order={order}
                orderOptions={orderOptions}
                setOrder={setOrder}
            />
            <div id="articles">
                <div id="heading">Event Articles</div>
                <Sidebar
                    sort={sort}
                    sortOptions={sortOptions}
                    setSort={setSort}
                    order={order}
                    orderOptions={orderOptions}
                    setOrder={setOrder}
                    mobile={true}
                />
                {articles.map(article => 
                    <Article key={article.articleId} article={article} />
                )}
            </div>
        </div>
    )
}
