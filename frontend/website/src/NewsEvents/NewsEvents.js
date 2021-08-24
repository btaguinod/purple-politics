import { useEffect, useState, useCallback } from 'react';
import { useLocation } from 'react-router';
import config from '../config';
import NewsEvent from './NewsEvent';
import Sidebar from '../Sidebar/Sidebar';
import './NewsEvents.css';

const useQuery = () => {
    return new URLSearchParams(useLocation().search).get('query');
};

const defaultSortOptions = ['Date', 'Companies'];
const defaultSortParams = {
    'Date': 'latestTime',
    'Companies': 'uniqueCompanies'
};
const searchSortOptions = ['Relevance', ...defaultSortOptions];
const searchSortParams = {'Relevance': 'relevance', ...defaultSortParams};
const orderOptions = ['Ascending', 'Descending'];
const orderParams = {
    'Ascending': 'true',
    'Descending': 'false'
};
const maxResults = 20;

export default function NewsEvents(props) {
    const query = useQuery();

    const [newsEvents, setNewsEvents] = useState([]);
    const [sort, setSort] = useState(query ? 'Relevance' : 'Date');
    const [order, setOrder] = useState('Descending');

    const [allLoaded, setAllLoaded] = useState(false);
    const [nextPageLoaded, setNextPageLoaded] = useState(false);
    const [page, setPage] = useState(1);

    useEffect(() => {
        setSort(query ? 'Relevance' : 'Date')
    }, [query])

    useEffect(() => {
        const abortController = new AbortController();
        const signal = abortController.signal;

        let sortParams = query ? searchSortParams : defaultSortParams;

        let sortQuery = 'sort=' + sortParams[sort];
        let orderQuery = 'ascending=' + orderParams[order];
        let maxResultsQuery = 'max=' + maxResults;
        let pageQuery = 'page=' + page;
        let searchQuery = query ? 'query=' + query : '';
        let queries = `?${sortQuery}&${orderQuery}&${maxResultsQuery}&${pageQuery}&${searchQuery}`;
        fetch(config.backendUrl + '/events' + queries, {signal})
            .then(response => response.json())
            .then(data => {
                let dataEvents = data['events'];
                setNewsEvents(prevEvents => prevEvents.concat(dataEvents));
                setNextPageLoaded(true);
                if (dataEvents.length < maxResults) 
                    setAllLoaded(true);
            })
            .catch(error => console.log(error));
        return () => abortController.abort()
    }, [order, sort, page, query]);

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
        setAllLoaded(false);
        setNewsEvents([]);
        setSort(newSort);
    };

    const updateOrder = newOrder => {
        setPage(1);
        setAllLoaded(false);
        setNewsEvents([]);
        setOrder(newOrder);
    };

    let sortOptions = query ? searchSortOptions : defaultSortOptions;
    let title = query ? `Search Results for "${query}"` : 'All Events';

    return (
        <div id="news-events-container">
            <Sidebar 
                sort={sort}
                sortOptions={sortOptions}
                setSort={updateSort}
                order={order}
                orderOptions={orderOptions}
                setOrder={updateOrder}
            />
            <div id="news-events">
                <div id="news-events-heading">{title}</div>
                <Sidebar 
                        sort={sort}
                        sortOptions={sortOptions}
                        setSort={updateSort}
                        order={order}
                        orderOptions={orderOptions}
                        setOrder={updateOrder}
                        mobile={true}
                />
                {newsEvents.map(newsEvent =>
                    <NewsEvent key={newsEvent.eventId} newsEvent={newsEvent} />
                )}
            </div>
        </div>
    );
}
