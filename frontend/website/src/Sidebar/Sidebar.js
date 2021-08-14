import './Sidebar.css'

export default function Sidebar(props) {
    let sort = props.sort
    const sortOptions = props.sortOptions
    let order = props.order
    const orderOptions = props.orderOptions

    const toButtonList = (options, choice, updateParent, mobile) => (
        options.map(option => {
            let className = "sidebar-button"

            if (mobile) {
                return (
                    <option className={className} key={option}>{option}</option>
                )
            }

            if (option === choice)
                className += " active"
            
            return (
                <button 
                    className={className}
                    key={option}
                    onClick={() => updateParent(option)}
                >
                    {option}
                </button>
            )
        })
    )

    const toButtons = (options, choice, updateParent, mobile) => {
        if (mobile) {
            return (
                <select 
                    className="sidebar-buttons" 
                    onChange={event => updateParent(event.target.value)}
                >
                    {toButtonList(options, choice, updateParent, mobile)}
                </select>
            );
        }
        return (
            <div className="sidebar-buttons">
                {toButtonList(options, choice, updateParent, mobile)}
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
