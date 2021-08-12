import { useState } from 'react';
import './SearchBar.css';

import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { 
    InstantSearch, 
    SearchBox, 
    Hits, 
    Highlight, 
    HitsPerPage
} from 'react-instantsearch-dom';
import algoliasearch from 'algoliasearch';

const searchClient = algoliasearch(
    'K2LSQ2DH6O', 
    'fe38ea3aa2a7be0b8ac3b8e2f69476e4'
)

export const Hit = ({hit}) => {
    let articleIndex = 0;
    for (;articleIndex < hit._highlightResult.articles.length; articleIndex++) {
        let article = hit._highlightResult.articles[articleIndex]
        if (article.title.matchLevel !== 'none')
            break;
    }
    return (
        <Link to={'/articles/' + hit.objectID}>
            <Highlight attribute={`articles[${articleIndex}].title`} hit={hit}/>
        </Link>
    );
};

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
                <Hits hitComponent={Hit} />
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
 