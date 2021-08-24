import { useState } from 'react';
import './Dropdown.css';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { faChevronUp } from '@fortawesome/free-solid-svg-icons';

export default function Dropdown(props) {
    const [active, setActive] = useState(false);

    const handleClick = option => { 
        props.updateParent(option);
        setActive(false)
    }

    let options = props.options.map(option => {
        let button;
        if (props.choice === option) {
            button = (
                <button 
                    className="dropdown-option active"
                    key={option}
                    onClick={() => setActive(false)}
                    onBlur={() => setActive(false)}
                >
                    {option}
                </button>
            )
        } else {
            button = (
                <button 
                    className="dropdown-option" 
                    key={option}
                    onClick={() => handleClick(option)}
                    onBlur={() => setActive(false)}
                >
                    {option}
                </button>
            )
        }
        return button
    })

    return (
        <div className="dropdown">
            <div 
                className="dropdown-choice"
                onClick={() => setActive(!active)}
            >
                {props.choice}
                <FontAwesomeIcon 
                    className="dropdown-icon"
                    icon={active ? faChevronUp : faChevronDown} 
                />
            </div>
            <div className="dropdown-options">{active ? options : ''}</div>
        </div>
    );
}
