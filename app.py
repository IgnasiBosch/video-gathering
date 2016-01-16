from src import store
from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 's3cr3t'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get-videos')
def get_videos():
    return jsonify({'data': list(store.find_all_videos())})


@app.route('/get-playlists')
def get_playlists():
    return jsonify({'data': list(store.find_all_playlists())})


@app.route('/get-sources')
def get_sources():
    return jsonify({'data': list(store.find_all_sources())})


if __name__ == '__main__':
    app.run(debug=True)


