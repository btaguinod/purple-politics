import './Sidebar.css'

export default function Sidebar(props) {
    let sort = props.sort
    const sortOptions = props.sortOptions
    let order = props.order
    const orderOptions = props.orderOptions

    const toButtons = (options, choice, updateParent) => {
        return options.map(option => {
            let className = "sidebar-button"
            if (option === choice)
                className += " active"

            return <button 
                className={className}
                key={option}
                onClick={() => updateParent(option)}
            >
                {option}
            </button>
        })
    }

    return (
        <div className={'sidebar' + (props.mobile ? ' mobile' : '')}>
            <div className="sidebar-heading">Sort</div>
            <div className="sidebar-buttons">
                {toButtons(sortOptions, sort, props.setSort)}
            </div>
            <div className="sidebar-buttons">
                {toButtons(orderOptions, order, props.setOrder)}
            </div>
        </div>
    )
}
