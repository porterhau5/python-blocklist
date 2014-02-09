#!/usr/bin/python
# -*- coding: utf-8 -*-

# scratch space... very much a work-in-progress

import hashlib
import urllib2

# Grab records from the text, write to flat file
def collect_IPs(text):
    # grab lines that begin with an IP address
    lines = [line for line in text.split('\n') if line.strip() and \
            line[0].isdigit()]
    # write records to flat file
    f = open_file("ips.txt", "a+")
    f.seek(0)
    ipcontent = f.read()
    for record in lines:
        recordcsv = str(record.split('\t')).strip('[').strip(']')
        recordcsv = str(recordcsv.split(',')[0:3] + recordcsv.split(',')[4:7]).strip('[').strip(']')
        recordhash = hashlib.sha256(recordcsv).hexdigest()
        if recordhash not in ipcontent:
            f.write(recordhash + ', ' + recordcsv + '\n')
    f.close()

# Compare the hash stored in hashfile with the message's hash
# Currently uses SHA256
def compare_hashes(hashfile, message):
    hashfile.seek(0)
    oldhash = hashfile.read()

    # hashfile is empty
    if oldhash == '':
        #print "oldhash is empty, recreating hash"
        # first, try to recreate hash from existing block.txt file
        f = open_file("block.txt", "a+")
        f.seek(0)
        text = f.read()
        # if block.txt is empty too, then we need to create both files
        if text != '':
            #print "block.txt was not empty"
            oldhash = hashlib.sha256(text).hexdigest()
            hashfile.write(oldhash)
        f.close()

    newhash = hashlib.sha256(message).hexdigest()
    #print "newhash: " + newhash
    #print "oldhash: " + oldhash
    if newhash == oldhash:
        print "Already at latest version.\n"
        hashfile.close()
        exit(0)
    else:
        print "New file available. Copying to filesystem.\n"
        hashfile.seek(0)
        hashfile.truncate()
        hashfile.write(newhash)
        hashfile.close()

# Download latest block list file from dshield.org
# Return the content of the file
def download_list():
    try:
        listfile = urllib2.urlopen("http://feeds.dshield.org/block.txt").read()
    except urllib2.HTTPError, e:
        print "There was an HTTP error."
        print e
        exit(0)
    except urllib2.URLError, e:
        print "There is a problem with the URL."
        print e
        exit(0)
    except IOError, e:
        print "There was an IOError."
        print e
        exit(0)
    else:
        return listfile

# Try to open file_name in mode
# If successful, return the opened file descriptor
def open_file(file_name, mode):
    try:
        the_file = open(file_name, mode)
    except IOError, e:
        print "Unable to open the file", file_name, "Exiting.\n", e
        exit(0)
    else:
        return the_file

def main():
    content = download_list()
    blockhash = open_file("block.sha256", "a+")
    blocklist = open_file("block.txt", "a+")
    blocklist.seek(0)

    if blocklist.read() == '':
        blocklist.write(content)
        blocklist.close()
        compare_hashes(blockhash, content)
    else:
        blocklist.close()
        compare_hashes(blockhash, content)
        blocklist = open_file("block.txt", "a+")
        blocklist.seek(0)
        blocklist.write(content)
        blocklist.close()

    collect_IPs(content)

if __name__ == '__main__':
    main()

# TODO:
# fix quotes in csv
# check for new IPs
# sort IPs in db
