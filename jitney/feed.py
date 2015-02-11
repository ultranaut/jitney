"""Handle the interactions with the GTFS feed."""

from urllib import urlretrieve as retrieve
import zipfile
import os
import csv

class Feed:

    def __init__(self, data_src=None):
        if data_src is None:
            data_src = 'http://www.ultranaut.com/gtfs/rail_data.zip'
        self.data_src = data_src

        instance = os.path.realpath(__file__)
        instance_dir = os.path.dirname(instance)
        self.data_dir = instance_dir + '/data'
        self.zipfile = self.data_dir + '/rail_data.zip'

    def retrieve(self):
        # grab the latest from njtransit
        res = retrieve(self.data_src, self.zipfile)

        # expand the archive
        zf = zipfile.ZipFile(self.zipfile)
        zf.extractall(self.data_dir + '/rail_data')

    def process(self):

        mysql = ""
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

