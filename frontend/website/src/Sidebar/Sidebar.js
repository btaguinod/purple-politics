import Dropdown from './Dropdown/Dropdown';
import './Sidebar.css';

export default function Sidebar(props) {
    let sort = props.sort
    const sortOptions = props.sortOptions
    let order = props.order
    const orderOptions = props.orderOptions

    const toButtonList = (options, choice, updateParent, mobile) => (
        options.map(option => {
            let button;
            if (option === choice) {
                button = (
                    <div 
                        className="sidebar-button active"
                        key={option}
                    >
                        {option}
                    </div>
                );
            } else {
                button = (
                    <button 
                        className={"sidebar-button"}
                        key={option}
                        onClick={ () => updateParent(option)}
                    >
                        {option}
                    </button>
                );
            }
                
            
            return button;
        })
    )

    const toButtons = (options, choice, updateParent, mobile) => {
        if (mobile) {
            return (
                <Dropdown
                    options={options}
                    choice={choice}
                    updateParent={updateParent}
                />
            );
        }
        return (
            <div className="sidebar-buttons">
                {toButtonList(options, choice, updateParent)}
            </div>
        );
    };

    return (
        <div className={'sidebar' + (props.mobile ? ' mobile' : '')}>
            <div className="sidebar-heading">Sort</div>
            {toButtons(sortOptions, sort, props.setSort, props.mobile)}
            {toButtons(orderOptions, order, props.setOrder, props.mobile)}
        </div>
    )
}
