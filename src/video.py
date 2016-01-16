import requests
from itertools import chain
from urllib import parse
from bs4 import BeautifulSoup
from src import source
from src import store
import sys

LIST_TYPE_PLAIN = 'plain_list'
LIST_TYPE_PLAY_LIST = 'play_list'


class VideoSource(object):
    def __init__(self, title, url, ref, source=None, playlists=None):
        if not playlists:
            playlists = []
        self.title = title
        self.url = url
        self.ref = ref
        self.source = source
        self.playlists = playlists

    def to_dict(self):
        self.source = self.source.__dict__
        return self.__dict__

    def is_valid(self):
        black_list = ['[Deleted Video]', '[Private Video]']
        return self.title not in black_list


def build_from_dict(_dict):
    _source = source.build_source_from_dict(_dict['source'])
    return VideoSource(title=_dict['title'], url=_dict['url'], ref=_dict['ref'], source=_source,
                       playlists=_dict['playlists'])


def get_videos_from_source(source):
    return chain(get_videos_from_playlists(source), get_videos_from_list(source))


def get_videos_from_playlists(source):
    link_more_selector = 'button.load-more-button'
    link_more_attribute_selector = 'data-uix-load-more-href'

    res = requests.get(source.url + '/playlists')
    html = res.text
    bs = BeautifulSoup(html, 'html.parser')
    domain = get_domain_name(source.url)

    if bs.select_one(link_more_selector):
        link_more = bs.select_one(link_more_selector)[link_more_attribute_selector]
        res = load_more_content(domain + link_more)
    else:
        res = {'link_more': False}

    lists = bs.select('div.yt-lockup-content a.yt-uix-sessionlink.spf-link')

    for _list in lists:
        playlists = [{'url': domain + _list['href'], 'title': _list.get_text().strip()}]
        for video in scrape_videos_from_list(domain + _list['href'], LIST_TYPE_PLAY_LIST):
            video.playlists = playlists
            if not video.source:
                video.source = source.__dict__
            yield video

    while res['link_more']:
        bs = BeautifulSoup(res['content'], 'html.parser')
        lists = bs.select('div.yt-lockup-content a.yt-uix-sessionlink.spf-link')
        for _list in lists:
            playlists = [{'url': domain + _list['href'], 'title': _list.get_text().strip()}]
            for video in scrape_videos_from_list(domain + _list['href'], LIST_TYPE_PLAY_LIST):
                video.playlists = playlists
                if not video.source:
                    video.source = source.__dict__
                yield video

        res = load_more_content(res['link_more'])


def get_videos_from_list(source):
    for video in scrape_videos_from_list(source.url + '/videos', LIST_TYPE_PLAIN):
        if not video.source:
            video.source = source.__dict__
        yield video


def scrape_videos_from_list(url, list_type):
    link_more_selector = 'button.load-more-button'
    link_more_attribute_selector = 'data-uix-load-more-href'

    res = requests.get(url)
    html = res.text
    bs = BeautifulSoup(html, 'html.parser')

    for video in get_video_from_items(bs, url, list_type):
        yield video

    domain = get_domain_name(url)
    if bs.select_one(link_more_selector):
        link_more = bs.select_one(link_more_selector)[link_more_attribute_selector]
        res = load_more_content(domain + link_more)
    else:
        res = {'link_more': False}

    while res['link_more']:
        bs = BeautifulSoup(res['content'], 'html.parser')
        for video in get_video_from_items(bs, url, list_type):
            yield video
        res = load_more_content(res['link_more'])


def get_video_from_items(bs, url, list_type):
    if list_type == LIST_TYPE_PLAY_LIST:
        return get_video_from_play_list_items(bs, url)
    else:
        return get_video_from_plain_list_items(bs, url)


def get_video_from_plain_list_items(bs, url):
    items = bs.find_all('a', {'class': 'yt-uix-tile-link'})
    for item in items:
        ref = get_video_ref_from_url(item['href'])
        video = VideoSource(title=item.get_text().strip(), url=get_domain_name(url) + item['href'], ref=ref)
        if video.is_valid():
            yield video


def get_video_from_play_list_items(bs, url):
    items = bs.find_all('td', {'class': 'pl-video-title'})
    for item in items:
        ref = get_video_ref_from_url(item.find('a')['href'])

        video = VideoSource(title=item.find('a').get_text().strip(), url=get_domain_name(url) + item.find('a')['href'],
                            ref=ref)

        if video.is_valid():
            owner_dom = item.find('div', {'class': 'pl-video-owner'})
            if owner_dom:
                source_dom = owner_dom.find('a')
                split_source_url = source.validate_url(get_domain_name(url) + source_dom['href'])
                _source = store.find_source_by_slug(split_source_url['slug'])
                if not _source:
                    _source = source.build_source_from_url(get_domain_name(url) + source_dom['href'])

                video.source = _source.__dict__

            yield video


def get_video_ref_from_url(url):
    try:
        return parse.parse_qs(parse.urlsplit(url).query)['v'][0]
    except KeyError:
        print('ERROR' + url)


def get_domain_name(url):
    return parse.urlunparse(parse.urlparse(url)[:2] + ('',) * 4)


def load_more_content(url):
    req = requests.get(url)
    res = req.json()

    if res['load_more_widget_html']:
        bs = BeautifulSoup(res['load_more_widget_html'], 'html.parser')
        link_more = get_domain_name(url) + bs.select_one('button.load-more-button')['data-uix-load-more-href']
    else:
        link_more = False

    return {'link_more': link_more, 'content': res['content_html']}
