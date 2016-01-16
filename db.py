import pkg_resources
from ming import create_datastore
from ming.odm import ThreadLocalODMSession

session = ThreadLocalODMSession(bind=create_datastore('video_gathering'))


try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
