import { useEffect, useState } from 'react'
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
const maxResults = 200

export default function NewsEvents() {
    const [newsEvents, setNewsEvents] = useState([])
    const [sort, setSort] = useState('Date')
    const [order, setOrder] = useState('Descending')

    useEffect(() => {
        let sortQuery = 'sort=' + sortParams[sort]
        let orderQuery = 'ascending=' + orderParams[order]
        let maxResultsQuery = 'max=' + maxResults
        let queries = '?' + sortQuery + '&' + orderQuery + '&' + maxResultsQuery
        fetch(config.backendUrl + '/events' + queries)
            .then(response => response.json())
            .then(data => {
                let dataNewsEvents = data['events']
                setNewsEvents(dataNewsEvents);
            })
    }, [order, sort])

    return (
        <div id="news-events-container">
            <Sidebar 
                sort={sort}
                sortOptions={sortOptions}
                setSort={setSort}
                order={order}
                orderOptions={orderOptions}
                setOrder={setOrder}
            />
            <div id="news-events">
                <div id="news-events-heading">All Events</div>
                <Sidebar 
                        sort={sort}
                        sortOptions={sortOptions}
                        setSort={setSort}
                        order={order}
                        orderOptions={orderOptions}
                        setOrder={setOrder}
                        mobile={true}
                />
                {newsEvents.map(newsEvent =>
                    <NewsEvent key={newsEvent.eventId} newsEvent={newsEvent} />
                )}
            </div>
        </div>
    )
}
