import sys
from src import source
from src import store
from src import video


def run(url):
    print('\n*** RUN %s *****************************\n' % url)
    _source = source.build_source_from_url(url)

    for _video in video.get_videos_from_source(_source):
        store.save_video(_video)
        print(_video.title)

    print('\n** END %s ******************************\n' % url)


if __name__ == "__main__":
    urls = sys.argv[1:]
    for url in urls:
        run(url)
