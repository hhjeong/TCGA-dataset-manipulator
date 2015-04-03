#!/usr/bin/python

import sys
from glob import glob
from os import path
from pprint import pprint
import logging 

logging.basicConfig( level=logging.INFO )

def match( genomeDataFile, clinDataFile ):

    matchedGenomeDataFile = genomeDataFile.replace('.txt','.matched.txt')

    matchedClinDataFile = clinDataFile.replace('.txt','.matched.txt')

    with open(genomeDataFile,'r') as inp:
        genomeHeader = inp.readline().rstrip().split('\t')
        genomeData = [ line.strip().split('\t') for line in inp.xreadlines() ]
        genomeSampleID = set( genomeHeader[1:] )

    with open(clinDataFile,'r') as inp:
        clinHeader = inp.readline().rstrip().split('\t')
        clinData = [ line.strip().split('\t') for line in inp.xreadlines() ]
        clinSampleID = set( [ c[0] for c in clinData ] )

    matchedSampleID = genomeSampleID & clinSampleID
    logging.info( "# samples in Genomic Matrix File = {0}".format( len(genomeSampleID) ) )
    logging.info( "# samples in Clinical Data File = {0}".format( len(clinSampleID) ) )
    logging.info( "Common Samples in both files = {0}".format( len(matchedSampleID) ) )

    # for convience of processing

    matchedSampleID.add( '' )
    with open(matchedGenomeDataFile,'w') as oup:
        keep = [ True if g in matchedSampleID else False for g in genomeHeader ]

        print >> oup, "\t".join( [ v for k, v in zip(keep, genomeHeader) if k ] )
        for row in genomeData:
            print >> oup, "\t".join( [ v for k,v in zip(keep,row) if k ]  )


    with open(matchedClinDataFile,'w') as oup:
        print >> oup, "\t".join( clinHeader )
        print >> oup, "\n".join( [ "\t".join(v) for v in clinData if v[0] in matchedSampleID ] )

    logging.info( "matching {0} and {1} is finished!".format( genomeDataFile, clinDataFile ) )

def main():

    clinPath = "*.clinical.txt"
    
    for clinDataFile in glob(clinPath):
        genomeDataFile = clinDataFile.replace('.clinical.txt','.genomicMatrix.txt') 
        if not path.exists( genomeDataFile ):
            logging.warning( "ERROR: {0} doesn't exist!".format( genomeDataFile ) )
        
        match( genomeDataFile, clinDataFile )

if __name__ == "__main__":
    main()
