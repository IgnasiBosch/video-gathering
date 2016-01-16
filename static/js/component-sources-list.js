/** @jsx React.DOM */

var SourcesList = React.createClass({

    getInitialState() {
        return {sources: []}

    },

    componentDidMount: function () {
        $.get('http://ignatius.linux:5000/get-sources', function (result) {
            if (this.isMounted()) {
                this.setState({
                    sources: result.data
                });
            }
        }.bind(this));
    },

    render() {
        return (
            <div className='sources'>
                <ul>
                    {
                        this.state.sources.map((source, i) => {
                            if(source == null)
                                return
                            return (
                                <li key={i}>
                                    <span>
                                        <a href={source.url} target="_blank">
                                            <img src={source.logo} title={source.name}/>
                                            {source.name}
                                        </a>
                                    </span>
                                </li>
                            );
                        })
                    }
                </ul>
            </div>
        );
    }
});


React.render(<SourcesList/>, document.getElementById('source-container'));
