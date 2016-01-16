
# Video Gathering

- Youtube Crawler to index all resources from youtube channels or users<br>
- Scrape main list and all playlists<br>
- Displayed in web page builded in Flask framework<br>
- Python 3.4<br>
- Flask<br>
- BeautifulSoup4<br>
- Ming<br>
- MongoDB<br>



### Clone project
`$ git clone https://github.com/IgnasiBosch/video-gathering.git`<br />
`$ cd video-gathering`

### Install pip - Python package management system (only if it's not installed)
`$ [sudo] apt-get install python-pip`

### Install virtualenv - Tool to create isolated Python environments (only if it's not installed)
`$ [sudo] pip install virtualenv`

### Create virtual environment:
`$ virtualenv -p /usr/bin/python3 venv`

### Activate shell script on virtual environment:
`$ source venv/bin/activate`

### Install dependencies:
`$ pip install -r requirements.txt`


## Run Crawler
`$ python manager.py <youtube url> [<youtube url> ...]`

## Run app server
`$ python app.py`

## Open your browser
`http://localhost:5000`