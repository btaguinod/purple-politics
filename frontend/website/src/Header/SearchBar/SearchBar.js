import { useState } from 'react';
import './SearchBar.css';

import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { 
    InstantSearch, 
    SearchBox, 
    connectHits,
    connectStateResults, 
    Highlight, 
    HitsPerPage
} from 'react-instantsearch-dom';
import algoliasearch from 'algoliasearch';

const searchClient = algoliasearch(
    'K2LSQ2DH6O', 
    'fe38ea3aa2a7be0b8ac3b8e2f69476e4'
)

const Hit = ({hit}) => {
    let articleIndex = 0;
    for (;articleIndex < hit._highlightResult.articles.length; articleIndex++) {
        let article = hit._highlightResult.articles[articleIndex]
        if (article.title.matchLevel !== 'none')
            break;
    }
    return (
        <Link className="ais-Hits-item" to={'/articles/' + hit.objectID}>
            <Highlight attribute={`articles[${articleIndex}].title`} hit={hit}/>
        </Link>
    );
};

const CustomHits = ({hits}) => (
    <div className="ais-Hits">
        {hits.map(hit => <div key={hit.objectID}>{Hit({hit})}</div>)}
        <a className="ais-Hits-img" href="https://www.algolia.com/">
            <img 
                src={`${process.env.PUBLIC_URL}/img/algolia.webp`} 
                alt="Search by Algolia"
            />
        </a>
    </div>
);

const Hits = connectHits(CustomHits);

const Results = connectStateResults(({searchState}) =>
    searchState && searchState.query ? (
        <Hits hitComponent={Hit} />
    ) : (
        ""
    )
);

export default function SearchBar(props) {
    const [showSearch, setShowSearch] = useState(props.className === 'mobile');

    const handleBlur = event => {
        if (event.relatedTarget === null) {
            if (props.className !== 'mobile')
                setShowSearch(false);
            return;
        }
        if (event.relatedTarget.tagName.toLowerCase() === 'a') {
            window.location.href = event.relatedTarget.href;
        }
    };

    let search;
    if (showSearch) {
        search = (
            <div className="search-bar"  onBlur={handleBlur}>
                <SearchBox autoFocus={true} translations={{placeholder: 'Search Events'}} />
                <FontAwesomeIcon icon={faSearch} className="search-icon" />
                <Results />
            </div>
        );
    } else {
        search = (
            <FontAwesomeIcon 
                icon={faSearch} 
                className="search-icon"
                onClick={() => setShowSearch(true)}
            />
        );
    }
    return (
        <InstantSearch
            searchClient={searchClient}
            indexName="purple_politics"
        >
            <HitsPerPage items={[]} defaultRefinement={5} />
            <div className={'search ' + props.className}>
                {search}
            </div>
        </InstantSearch>
    );
}
 