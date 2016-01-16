from db import session
from src import source


def save_video(new_video):
    _video = session.db.videos.find_one({'ref': new_video.ref})
    if not _video:
        return session.db.videos.insert(new_video.__dict__)
    else:
        __video = find_video_by_ref_and_playlist(new_video)
        if not __video:
            resulting_list = list(_video['playlists'])
            resulting_list.extend(x for x in new_video.playlists if x not in resulting_list)
            new_video.playlists = resulting_list
            return session.db.videos.update({'_id': _video['_id']}, {'$set': new_video.__dict__})

        return None


def find_all_videos():
    for v in session.db.videos.find({}, {'_id': 0}):
        yield v


def find_video_by_ref_and_playlist(_video):
    if not len(_video.playlists):
        return _video
    try:
        return session.db.videos.find_one({'ref': _video.ref, 'playlists': {'$elemMatch': _video.playlists[0]}})
    except Exception as e:
        print(e)
        print(_video)
        print(_video.playlists)


def find_source_by_slug(slug):
    _v = session.db.videos.find_one({'source.slug': slug})
    if _v:
        return source.build_source_from_dict(_v['source'])
    else:
        return None


def find_all_sources():
    return session.db.videos.distinct("source")


def find_all_playlists():
    return session.db.videos.distinct('playlists')
