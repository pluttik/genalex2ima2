import sqlite3
import string

dbname = raw_input('Enter database name (default is testout.sqlite): ')
if ( len(dbname) < 1 ) : dbname = 'testout.sqlite'

#make and open a file that will contain all the ima2 infile filenames
filenamesfile = 'filenamesfile.txt'
fnf_handle = open(filenamesfile,'w')

conn = sqlite3.connect(dbname)
cur = conn.cursor()

#find the loci and the populations
loci=list()
pops=list()
cur.execute('SELECT name FROM location ORDER BY name')
names=cur.fetchall()
for name in names:
    pops.append(str(name[0]))
cur.execute('SELECT name FROM loci ORDER BY name')
names=cur.fetchall()
for name in names:
    loci.append(str(name[0]))

#iterate over all population pairs
popAcount=0
popsB=pops
for popA in pops:
    popBcount=0
    for popB in popsB:
        if popAcount<popBcount:
            #make and open the outfile
            fname = popA+popB+'_infile.txt'
            #write this new filename to the filenamesfile
            fnf_handle.write('%s\n' % (fname))
            #print fname
            handle = open(fname,'w')
            infile_body=str()
            no_loci=0
            
            #iterate over all loci
            for locus in loci:
                #print locus
                #find the observed alleles for this locus
                sql='''SELECT 
                           individual.name, 
                           '''+locus+'''.nrepeats, 
                           location.name 
                       FROM 
                           individual 
                           JOIN '''+locus+''' ON individual.'''+locus+'''a_id='''+locus+'''.id
                           JOIN location ON individual.location_id=location.id
                       WHERE 
                           ('''+locus+'''.lenbp<>"0")
                           AND (location.name="'''+popA+'''" OR location.name="'''+popB+'''")
                           '''
                cur.execute(sql)
                namesA = cur.fetchall()

                sql='''SELECT 
                           individual.name, 
                           '''+locus+'''.nrepeats, 
                           location.name 
                       FROM 
                           individual 
                           JOIN '''+locus+''' ON individual.'''+locus+'''b_id='''+locus+'''.id
                           JOIN location ON individual.location_id=location.id
                       WHERE 
                           ('''+locus+'''.lenbp<>"0")
                           AND (location.name="'''+popA+'''" OR location.name="'''+popB+'''")
                           '''    
                cur.execute(sql)
                namesB = cur.fetchall()
                
                
                #count the number in popA and popB from namesA and namesB
                no_allelespopA=0
                no_allelespopB=0
                for nameA in namesA:
                    if nameA[2] == popA:
                        no_allelespopA = no_allelespopA + 1
                    if nameA[2] == popB:
                        no_allelespopB = no_allelespopB + 1
                for nameB in namesB:
                    if nameB[2] == popB:
                        no_allelespopB = no_allelespopB + 1
                    if nameB[2] == popA:
                        no_allelespopA = no_allelespopA + 1
                
                
                #discard the locus if the number of alleles in popA or popB <20
                if no_allelespopA>19 and no_allelespopB>19:
                    no_loci = no_loci+1
                    infile_popAalleles = str()
                    infile_popBalleles = str()
                    #write the first line for the locus, e.g.: Med367 82 82 1 S 1.00 0.002
                    infile_body=infile_body+'%s %d %d 1 S 1.00 0.002\n' % (locus, no_allelespopA, no_allelespopB)
                    #fill outfile with the data for the locus
                    for nameA in namesA:
                        nameA_long = nameA[0]
                        while len(nameA_long)<9: nameA_long = nameA_long + '0'
                        #print nameA_long,nameA[1]
                        if nameA[2] == popA:
                            infile_popAalleles=infile_popAalleles+'%s %s\n' % (nameA_long,nameA[1])
                        if nameA[2] == popB:
                            infile_popBalleles=infile_popBalleles+'%s %s\n' % (nameA_long,nameA[1])
                    for nameB in namesB:
                        nameB_long = nameB[0]
                        while len(nameB_long)<9: nameB_long = nameB_long + '0'
                        #print nameB_long,nameB[1]
                        if nameB[2] == popA:
                            infile_popAalleles=infile_popAalleles+'%s %s\n' % (nameB_long,nameB[1])
                        if nameB[2] == popB:
                            infile_popBalleles=infile_popBalleles+'%s %s\n' % (nameB_long,nameB[1])
                    infile_body = infile_body + infile_popAalleles + infile_popBalleles
            #write the outfile
            #fill the header of the outfile
            handle.write('M. edulis infile Ima2\n2\n%s %s\n(0,1):2\n%d\n' % (popA,popB,no_loci))
            #warning printed to screen if for this file the no_loci is zero
            if no_loci<1: print 'WARNING: no loci with sufficient data for',fname
            handle.write(infile_body)
            #close the outfile
            handle.close()
        popBcount=popBcount+1
    popAcount=popAcount+1
fnf_handle.close()    