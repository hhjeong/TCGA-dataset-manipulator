#!/usr/bin/python
import sys, glob, os
import logging
from pprint import pprint

logging.basicConfig( level=logging.INFO )

for folder in glob.glob("TCGA_*"):

    clinDataFile = os.path.join( folder, "clinical_data" )

    genomeDataFile = os.path.join( folder, "genomicMatrix" )

    
    profileName = folder.replace('TCGA_','').split('-')[0]

    if not os.path.exists( clinDataFile ):
        logging.warning( "not found : {0}".format( clinDataFile ) )
        continue
    if not os.path.exists( genomeDataFile ):
        logging.warning( "not found : {0}".format( genomeDataFile ) )
        continue

    with open( clinDataFile, 'r' ) as inp:
        header = inp.readline().replace('\n','').split('\t')
        
        lstTarget = ["sampleID", "days_to_birth", "_OS", "_OS_IND"]
        printTarget = [ "", "age", "os", "ind" ]
        target = set( lstTarget )

        outClinFile = '{0}.clinical.txt'.format( profileName )

        with open( outClinFile, 'w' ) as oup:
            print >> oup, "\t".join( printTarget )
            for row in inp.readlines():
                row = row.split('\t')
                sampleInfo = dict([ (h,v) for h,v in zip(header,row) if h in target ])

                if  '' in set(sampleInfo.values()):
                    continue

                sampleInfo['days_to_birth'] = "%d" % -int(sampleInfo['days_to_birth']) 
                print >> oup, "\t".join( [ sampleInfo[t] for t in lstTarget ] )
               
        logging.info( "FINISHED : {0}".format( outClinFile ) )

    with open( genomeDataFile, 'r' ) as inp:
        outGenomeFile = '{0}.genomicMatrix.txt'.format( profileName )

        with open( outGenomeFile, 'w' ) as oup:
            header = inp.readline().strip().split('\t')
            header[0] = ''

            print >> oup, "\t".join(header)

            for row in inp.xreadlines():
                print >> oup, row.strip()

        logging.info( "FINISHED : {0}".format( outGenomeFile ) )
        

