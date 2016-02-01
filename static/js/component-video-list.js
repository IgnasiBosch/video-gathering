/** @jsx React.DOM */

var VideoList = React.createClass({

    getInitialState() {
        return {videos: []}

    },

    componentDidMount: function () {
        $.get('/get-videos', function (result) {
            if (this.isMounted()) {
                this.setState({
                    videos: result.data
                });
            }
        }.bind(this));
    },

    render() {
        return (
            <div className='videos'>
                <ul>
                    {
                        this.state.videos.map((video, i) => {
                            if (video.playlists.length) {
                                playlistLink = <div><a href={video.playlists[0].url}
                                                        target="_blank">{video.playlists[0].title}</a></div>
                            } else {
                                playlistLink = null
                            }
                            if(video.source == null){
                                console.log(video)
                                return
                            }
                            return (
                                <li key={i}>
                                    <span>
                                        <a href={video.source.url} target="_blank">
                                            <img src={video.source.logo} title={video.source.name}/>
                                        </a>
                                    </span>
                                    <span>
                                        <a href={video.url} target="_blank">{video.title}</a>
                                        {playlistLink}
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


React.render(<VideoList/>, document.getElementById('video-container'));

