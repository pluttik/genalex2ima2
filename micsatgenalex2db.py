import sqlite3
import string

fname = raw_input('Enter infile name (default is test.csv): ')
if ( len(fname) < 1 ) : fname = 'test.csv'

dbname = raw_input('Enter database name (default is testout.sqlite): ')
if ( len(dbname) < 1 ) : dbname = 'testout.sqlite'

conn = sqlite3.connect(dbname)
cur = conn.cursor()

# Drop old tables, make the fixed tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS individual;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS loci;

CREATE TABLE location (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE loci (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE individual (
    id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name         TEXT UNIQUE,
    location_id  INTEGER
);

''')

# the first two lines of a typical GenAlEx file look like this:
# Sampleno,Pop,Loc01,,Loc02,,Loc03,,Loc04,,Loc05,,Loc06,,Loc07,,Loc08,
# Pop01Ind01,Pop01,213,216,146,146,180,180,166,171,180,180,143,180,0,0,187,217

#open the input file
handle = open(fname)

# find the loci in first row of file
count=0
loci=list()
for line in handle:
    if count<1:
        line=line.translate(None,'\n')
        elements=line.split(',')
        for element in elements:
            if element<>'':
                loci.append(element)
        count=count+1
handle.close()
loci=loci[2:]

#make variable sql tables for all loci and add foreign keys to table individual
for locus in loci:
    cur.execute('INSERT INTO loci (name) VALUES ( ? )', (locus,))
    sql='DROP TABLE IF EXISTS '+locus
    print sql
    cur.execute(sql)
    sql='CREATE TABLE  '+locus+' (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, lenbp   TEXT UNIQUE, nrepeats INTEGER UNIQUE)'
    cur.execute(sql)
    sql='ALTER TABLE individual ADD COLUMN '+locus+'a_id TEXT'
    cur.execute(sql)
    sql='ALTER TABLE individual ADD COLUMN '+locus+'b_id TEXT'
    cur.execute(sql)


handle=open(fname)
count=0
totnalleles=2*len(loci)

#read allele data from all but first line in csv
for line in handle: #per line find all the things to commit to SQL
    if count>0:
        line=line.translate(None,'\n')
        elements=line.split(',')
        #add pop and ind to the location and individual tables, also the foreign key
        pop=elements[1]
        ind=elements[0]
        cur.execute('''INSERT OR IGNORE INTO location (name) VALUES ( ? )''',(pop, ))
        cur.execute('SELECT id FROM location WHERE name = ? ', (pop, ))
        location_id = cur.fetchone()[0]
        cur.execute('''INSERT OR IGNORE INTO individual (name,location_id) VALUES ( ?,? )''',(ind, location_id))
        conn.commit()  
        #now you have the data for one individual, put this in the locus tables, also the foreign keys
        countloci=0
        countelements=0
        for element in elements[2:]:
            sql='INSERT OR IGNORE INTO '+loci[countloci]+'(lenbp) VALUES ('+element+')'
            print sql
            cur.execute(sql)
            conn.commit()
            sql='SELECT id FROM '+loci[countloci]+' WHERE lenbp = "'+element+'"'
            print sql
            cur.execute(sql)
            #allele_id is the foreign key to go into the table individual
            allele_id=cur.fetchone()[0]
            print 'allele_id:',allele_id
            if countelements%2==0:
                allelenameid=loci[countloci]+'a_id'
            else:
                allelenameid=loci[countloci]+'b_id'
            sql='UPDATE individual SET '+allelenameid+'="'+str(allele_id)+'" WHERE name="'+ind+'"'
            print sql
            cur.execute(sql)
            conn.commit()
            if countelements%2 == 1: countloci = countloci+1
            countelements=countelements+1
    count=count+1

#re-code lenbp to nrepeats for each locus abd write nrepeats to sqlite database
for locus in loci:
    print ''
    sql='SELECT * FROM '+locus+' ORDER BY lenbp'
    print sql
    cur.execute(sql)
    allele_list=cur.fetchall()
    allele_n = 0
    nrepeat_name = 5
    for allele in allele_list:
        print allele_list[allele_n]
        sql='SELECT id FROM '+locus+' WHERE lenbp="'+str(allele_list[allele_n][1])+'"'
        print sql
        cur.execute(sql)
        allele_id=cur.fetchone()[0]
        print 'allele_id=',allele_id
        sql='UPDATE '+locus+' SET nrepeats="'+str(nrepeat_name)+'" WHERE id="'+str(allele_id)+'"'
        print sql
        cur.execute(sql)
        conn.commit()
        allele_n = allele_n+1
        nrepeat_name = nrepeat_name+1