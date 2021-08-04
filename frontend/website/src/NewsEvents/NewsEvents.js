import { useEffect, useState, useCallback } from 'react'
import config from '../config'
import NewsEvent from './NewsEvent'
import Sidebar from '../Sidebar/Sidebar'
import './NewsEvents.css'

const sortOptions = ['Date', 'Companies']
const sortParams = {
    'Date': 'latestTime',
    'Companies': 'uniqueCompanies'
}
const orderOptions = ['Ascending', 'Descending']
const orderParams = {
    'Ascending': 'true',
    'Descending': 'false'
}
const maxResults = 20

export default function NewsEvents() {
    const [newsEvents, setNewsEvents] = useState([])
    const [sort, setSort] = useState('Date')
    const [order, setOrder] = useState('Descending')

    const [allLoaded, setAllLoaded] = useState(false)
    const [nextPageLoaded, setNextPageLoaded] = useState(false)
    const [page, setPage] = useState(1)

    useEffect(() => {
        let sortQuery = 'sort=' + sortParams[sort];
        let orderQuery = 'ascending=' + orderParams[order];
        let maxResultsQuery = 'max=' + maxResults;
        let pageQuery = 'page=' + page;
        let queries = '?' + sortQuery + '&' + orderQuery + '&' + maxResultsQuery + '&' + pageQuery;
        fetch(config.backendUrl + '/events' + queries)
            .then(response => response.json())
            .then(data => {
                let dataEvents = data['events']
                setNewsEvents(prevEvents => prevEvents.concat(dataEvents));
                setNextPageLoaded(true)
                if (dataEvents.length < maxResults) 
                    setAllLoaded(true);
            })
            .catch(error => console.error(error))
    }, [order, sort, page])

    const handleScroll = useCallback(() => {
        let scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
        let distToBottom = document.documentElement.scrollHeight - 
                           document.documentElement.clientHeight - 
                           scrollTop;
        if (distToBottom < 50 && !allLoaded && nextPageLoaded) {
            setNextPageLoaded(false)
            setPage(page + 1)
        }
    }, [nextPageLoaded, allLoaded, page])


    useEffect(() => {
        window.addEventListener('scroll', handleScroll)
        return () => window.removeEventListener('scroll', handleScroll)
    }, [handleScroll])

    const updateSort = newSort => {
        setPage(1)
        setNewsEvents([])
        setSort(newSort)
    }

    const updateOrder = newOrder => {
        setPage(1)
        setNewsEvents([])
        setOrder(newOrder)
    }

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
                <div id="news-events-heading">All Events</div>
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
    )
}
