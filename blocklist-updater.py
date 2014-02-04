#!/usr/bin/python
# -*- coding: utf-8 -*-

# scratch space... very much a work-in-progress

import hashlib
import urllib2

def compareHashes(hashfile, message):
    hashfile.seek(0)
    oldhash = hashfile.read()

    # hashfile is empty
    if oldhash == '':
        print "oldhash is empty, recreating hash"
        # first, try to recreate hash from existing block.txt file
        f = open_file("block.txt", "a+")
        f.seek(0)
        text = f.read()
        # if block.txt is empty too, then we need to create both files
        if text != '':
            print "block.txt was not empty"
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

def downloadList():
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

def open_file(file_name, mode):
    try:
        the_file = open(file_name, mode)
    except IOError, e:
        print "Unable to open the file", file_name, "Exiting.\n", e
        exit(0)
    else:
        return the_file

def main():
    content = downloadList()
    blockhash = open_file("block.sha256", "a+")
    blocklist = open_file("block.txt", "a+")
    blocklist.seek(0)
    if blocklist.read() == '':
        blocklist.write(content)
        blocklist.close()
        compareHashes(blockhash, content)
    else:
        blocklist.close()
        compareHashes(blockhash, content)
        blocklist = open_file("block.txt", "a+")
        blocklist.seek(0)
        blocklist.write(content)
        blocklist.close()

if __name__ == '__main__':
    main()

# TODO:
# check for new IPs
# write new IPs to db
# sort IPs in db
