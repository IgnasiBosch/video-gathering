import requests
import re
from bs4 import BeautifulSoup


class Source(object):
    def __init__(self, name, type, url, slug, logo=None):
        self.name = name
        self.type = type
        self.url = url
        self.slug = slug
        self.logo = logo


def build_source_from_dict(_dict):
    return Source(name=_dict['name'], type=_dict['type'], url=_dict['url'], slug=_dict['slug'], logo=_dict['logo'])


def build_source_from_url(url):
    split_url = validate_url(url)
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    name = get_name_from_bs(soup)
    logo = get_logo_from_bs(soup)

    source = Source(name=name, url=url, type=split_url['type'], slug=split_url['slug'], logo=logo)

    return source


def get_name_from_bs(bs):
    name_selector = 'a.branded-page-header-title-link'
    name_dom = bs.select_one(name_selector)
    if name_dom:
        return name_dom.text
    return None


def get_logo_from_bs(bs):
    logo_selector = 'img.channel-header-profile-image'
    logo_dom = bs.select_one(logo_selector)
    if logo_dom:
        return logo_dom['src']
    return None


def validate_url(url):
    valid_source_url = re.compile(r"https?://(?:www.)?youtube.(?:\w+)/(user|channel)/(\S+)")
    re_url = valid_source_url.match(url)
    if re_url:
        return {"type": re_url.group(1), "slug": re_url.group(2)}
    else:
        raise ConnectionError('Invalid url')
