"""Handle the interactions with the GTFS feed."""

from urllib import urlretrieve as retrieve
import zipfile
import os
import csv

class Feed:

    def __init__(self):

        instance = os.path.realpath(__file__)

        self.feed_uri = 'http://www.ultranaut.com/gtfs/rail_data.zip'
        self.raw_data = None;

        self.data_dir = os.path.dirname(instance) + '/data'
        self.zipfile = self.data_dir + '/rail_data.zip'

    def fetch(self):
        # grab the latest from njtransit
        res = retrieve(self.feed_uri, self.zipfile)

        # expand the archive
        zf = zipfile.ZipFile(self.zipfile)
        zf.extractall(self.data_dir + '/rail_data')

    def process(self):
        output = open(self.data_dir + '/rail.sql', 'w')

        for fn in ['agency', 'calendar_dates', 'routes', 'stop_times', 'stops', 'trips']:
            inserts = []
            currfile = self.data_dir + '/rail_data/' + fn

            with open(currfile+'.txt', 'rb') as csvfile:
                data = csv.reader(csvfile, delimiter=',', quotechar='"')
                headers_read = False
                # mysql = 'insert into `%s` ' % (fn)
                output.write('insert into `%s` ' % (fn))
                for row in data:
                    if not headers_read:
                        output.write('(`%s`) values\n' % ('`, `'.join(row)))
                        headers_read = True
                    else:
                        inserts.append('("%s")' % ('", "'.join(row)))
                output.write(',\n'.join(inserts) + ';\n')
                csvfile.close()
        # print mysql

    def store(self):
        pass


