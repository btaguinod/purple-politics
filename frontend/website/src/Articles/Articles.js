import { useEffect, useState, useCallback } from 'react';
import Article from './Article';
import Sidebar from '../Sidebar/Sidebar';
import './Articles.css';
import { nanoid } from 'nanoid';

import config from '../config';

const sortOptions = ['Date', 'Bias'];
const sortParams = {
    'Date': 'time',
    'Bias': 'bias'
};
const orderOptions = ['Ascending', 'Descending'];
const orderParams = {
    'Descending': 'false',
    'Ascending': 'true'
    
};
const maxResults = 10;

export default function Articles(props) {
    const [articles, setArticles] = useState([]);
    const [sort, setSort] = useState('Date');
    const [order, setOrder] = useState('Descending');

    const [allLoaded, setAllLoaded] = useState(false);
    const [nextPageLoaded, setNextPageLoaded] = useState(false);
    const [page, setPage] = useState(1);

    useEffect(() => {
        let eventId = props.match.params.eventId;
        let sortQuery = 'sort=' + sortParams[sort];
        let orderQuery = 'ascending=' + orderParams[order];
        let maxResultsQuery = 'max=' + maxResults;
        let pageQuery = 'page=' + page;
        let queries = '?' + sortQuery + '&' + orderQuery + '&' + pageQuery + 
            '&' + maxResultsQuery;
        fetch(config.backendUrl + '/articles/' + eventId + queries)
            .then(response => response.json())
            .then(data => {
                let dataArticles = data['articles'];
                for (let article of dataArticles) 
                    article['articleId'] = nanoid();
                setArticles(prevArticles => prevArticles.concat(dataArticles));
                setNextPageLoaded(true);
                if (dataArticles.length < maxResults) 
                    setAllLoaded(true);
            });
    }, [order, sort, page, props.match.params.eventId]);

    const handleScroll = useCallback(() => {
        let scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
        let distToBottom = document.documentElement.scrollHeight - 
                           document.documentElement.clientHeight - 
                           scrollTop;
        if (distToBottom < 50 && !allLoaded && nextPageLoaded) {
            setNextPageLoaded(false);
            setPage(page + 1);
        }
    }, [nextPageLoaded, allLoaded, page]);


    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, [handleScroll]);

    const updateSort = newSort => {
        setPage(1);
        setArticles([]);
        setSort(newSort);
    };

    const updateOrder = newOrder => {
        setPage(1);
        setArticles([]);
        setOrder(newOrder);
    };

    return (
        <div id="articles-container">
            <Sidebar
                sort={sort}
                sortOptions={sortOptions}
                setSort={updateSort}
                order={order}
                orderOptions={orderOptions}
                setOrder={updateOrder}
            />
            <div id="articles">
                <div id="heading">Event Articles</div>
                <Sidebar
                    sort={sort}
                    sortOptions={sortOptions}
                    setSort={updateSort}
                    order={order}
                    orderOptions={orderOptions}
                    setOrder={updateOrder}
                    mobile={true}
                />
                {articles.map(article => 
                    <Article key={article.articleId} article={article} />
                )}
            </div>
        </div>
    );
}
