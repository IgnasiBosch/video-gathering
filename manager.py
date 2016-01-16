import sys
from src import source
from src import store
from src import video



def run(url):
    print('run %s' % url)
    _source = source.build_source_from_url(url)

    for _video in video.get_videos_from_source(_source):
        store.save_video(_video)
        print(_video.title)

    print('end %s' % url)


urls = [
    'https://www.youtube.com/user/PyDataTV',
    # 'https://www.youtube.com/channel/UCkd1iKSCgfsK2xpIDExhg9A',
    # 'https://www.youtube.com/channel/UCgxzjK6GuOHVKR_08TT4hJQ',
    # 'https://www.youtube.com/channel/UCEBb1b_L6zDS3xTUrIALZOw',
    'https://www.youtube.com/user/MIT',
    # 'https://www.youtube.com/user/stanfordonline/featured',
    # 'https://www.youtube.com/user/TEDtalksDirector',
    # 'https://www.youtube.com/user/TEDxTalks',
    'https://www.youtube.com/channel/UCQ7dFBzZGlBvtU2hCecsBBg',
    # 'https://www.youtube.com/channel/UC98CzaYuFNAA_gOINFB0e4Q',
    # 'https://www.youtube.com/channel/UCkQX1tChV7Z7l1LFF4L9j_g',
    # 'https://www.youtube.com/channel/UCP_lo1MFyx5IXDeD9s_6nUw'
    # 'https://www.youtube.com/user/IGNASIBOSCH',
    # 'https://www.youtube.com/user/SlavojZizekVideos',
    # 'https://www.youtube.com/channel/UCkd1iKSCgfsK2xpIDExhg9A',
    'https://www.youtube.com/user/bigthink',
    'https://www.youtube.com/channel/UC4BRC9SMH8slKXtg9CY7U4w',
    'https://www.youtube.com/channel/UCBVCi5JbYmfG3q5MEuoWdOw',
    'https://www.youtube.com/channel/UChy_3ir-ESf0Y5b5j95J61A'

    # 'https://www.youtube.com/user/theyearinreview',
    # 'https://www.youtube.com/channel/UCbe1jMaBsndRL27wr4OOhQQ'

]

if __name__ == "__main__":
    for url in urls:
        run(url)
