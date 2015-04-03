#!/usr/bin/python

from glob import glob
from collections import defaultdict 

profile = defaultdict( lambda: defaultdict( int ) )

for fname in sorted( glob( "*.matched.txt" ) ):
    line_cnt = sum( 1 for _ in open(fname) )
    
    ptype, dtype = fname.replace('.txt','').split('.')[:2]

    nt = 'ns' if dtype == "clinical" else 'nf' 

    profile[ptype][nt] = line_cnt - 1

with open('summary.txt','w') as oup:
    for p in sorted(profile):
        print >> oup, "{0}\t{1}\t{2}".format( p, profile[p]['nf'], profile[p]['ns'] )
