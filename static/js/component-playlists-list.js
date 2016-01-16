/** @jsx React.DOM */

var PlayLists = React.createClass({

    getInitialState() {
        return {playlists: []}

    },

    componentDidMount: function () {
        $.get('http://ignatius.linux:5000/get-playlists', function (result) {
            if (this.isMounted()) {
                this.setState({
                    playlists: result.data
                });
            }
        }.bind(this));
    },

    render() {
        return (
            <div className='playlists'>
                <ul>
                    {
                        this.state.playlists.map((playlist, i) => {
                            return (
                                <li key={i}>
                                    <span>
                                        <a href={playlist.url} target="_blank">
                                            {playlist.title}
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


React.render(<PlayLists/>, document.getElementById('playlist-container'));

