import json

from pprint import pprint

from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import os
import requests
import shutil

def fetchData( fname ):
    print "fetching: ", fname
    url = "https://genome-cancer.ucsc.edu/download/public/%s.tgz" % fname
    r = requests.get( url, stream=True )
    chunk_size = 1024  

    print r
    with open("ready/%s.tgz"%fname, 'wb') as oup:
        for chunk in r.iter_content(chunk_size):
            oup.write(chunk)


with open('cancer_browser_dataset.json','r') as inp:
    jsonData = json.load(inp)

with open('cancer_browser_dataset.txt','w') as oup:
    keys = [ "domain", "cohort", "name", "longlabel", "name", "version" ]
    print >> oup, "\t".join(keys)
    fname = []
    for row in jsonData:
        row = dict(row)
        shorten = dict( [ (k,row[k]) for k in keys ] )
        fname.append( shorten["name"].replace("genomic_","") + "-" + shorten["version"] )
    pool = Pool(20)
    pool.map( fetchData, fname )
