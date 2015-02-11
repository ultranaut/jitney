"""Handle the interactions with the GTFS feed."""

from urllib import urlretrieve as retrieve
import zipfile

class Feed:


    def __init__(self):
        self.DATA_URI = 'http://www.ultranaut.com/gtfs'
        pass

    def retrieve(self):
        res = retrieve(self.DATA_URI + '/rail_data.zip', '/Users/ultranaut/Projects/jitney/jitney/data/rail_data.zip')

        pass
