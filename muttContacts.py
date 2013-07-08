#!/usr/bin/env python
# encoding: utf-8

from AddressBook import *
from subprocess import call
import sys
import pprint
import re
import getopt

def addressBook():

    ab = ABAddressBook.sharedAddressBook()
    people = ab.people()

    peopleList = []

    for person in people:
        thisPerson = {}
        props = person.allProperties()

        for prop in props:

            # skip some properties
            if prop == "com.apple.ABPersonMeProperty":
                continue
            elif prop == "com.apple.ABImageData":
                continue

            # How we convert the value depends on the ObjC
            # class used to represent it
            val = person.valueForProperty_(prop)
            if type(val) == objc.pyobjc_unicode:
                # Unicode String
                thisPerson[prop.lower()] = val
            elif type(val) == ABMultiValueCoreDataWrapper:
                # List -- convert each item in the list
                # into the proper format
                thisPerson[prop.lower()] = []
                for valIndex in range(0, val.count()):
                    indexedValue = val.valueAtIndex_(valIndex)
                    if type(indexedValue) == objc.pyobjc_unicode:
                        # Unicode string
                        thisPerson[prop.lower()].append(indexedValue)
                    elif type(indexedValue) == NSCFDictionary:
                        # NSDictionary -- convert to a Python Dictionary
                        propDict = {}
                        for propKey in indexedValue.keys():
                            propValue = indexedValue[propKey]
                            propDict[propKey.lower()] = propValue
                            thisPerson[prop.lower()].append(propDict)
        peopleList.append(thisPerson)
    return peopleList


def main(name, muttQuery):
    # if muttQuery is TRUE, print all email results
    myList = addressBook()
    i = 0
    hits = []
    while 1:
        while i < len(myList):
            thisName = ""
            if 'first' in myList[i]:
                thisName = "%s" % myList[i]['first']
            if 'last' in myList[i]:
                thisName = "%s %s" % (thisName, myList[i]['last'])

            if re.search(name, thisName, flags=2):
                if 'email' in myList[i]:
                    hits.append([thisName, myList[i]])
            i += 1

        i = 0
        if muttQuery == 1:
            break
        theList = ""
        while i < len(hits):
            line = "%d | %s" % (i, hits[i][0])
            theList = "%s\n%s" % (theList, line)
            i += 1

        if len(theList) == 0:
            name = raw_input("No results.  Enter a new name ([q]uit): ")
            if name == 'q' or name == 'Q':
                sys.exit(0)
        else:
            break

    while 1:
        if muttQuery == 1:
            break
#        print theList
        ans = raw_input("Which person? ([q]uit) ")
        if ans == '':
            ans = 0
        elif ans == 'q' or ans == 'Q':
            sys.exit(0)

        if int(ans) < len(theList):
            ans = int(ans)
            break
    if muttQuery == 1:
        output = ''
        count = 0
        for result in hits:
            for address in result[1]['email']:
                count += 1
                line = "\"%s\"\t%s" % (address, result[0])
                if output == '':
                    output = "%s" % (line)
                else:
                    output = "%s \n%s" % (output, line)

        print count
        print output
    elif len(hits[ans][1]['email']) > 1:
        i = 0
        theList = ""
        while i < len(hits[ans][1]['email']):
            line = "%d | %s" % (i, hits[ans][1]['email'][i])
            theList = "%s\n%s" % (theList, line)
            i += 1

        while 1:
            print theList
            esel = raw_input("Which address? ([q]uit)")
            if esel == '':
                esel = 0
            elif esel == 'q' or esel == 'Q':
                sys.exit(0)
            if int(esel) < len(theList):
                esel = int(esel)
                MUTT(hits[ans][0], hits[ans][1]['email'][esel])
                break

    else:
        MUTT(hits[ans][0], hits[ans][1]['email'][0])


def MUTT(name, address):
    call(["/usr/local/bin/mutt", "\"%s\" <%s>" % (name, address)])


def USAGE():
    print "usage: %s query" % sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 1:
        USAGE()
        sys.exit(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hms:",
                    ["help", "mutt", "search="])
    except getopt.GetoptError as err:
        print str(err)
        USAGE()
        sys.exit(1)
    QUERY = 0
    searchname = ''
    for o, a in opts:
        if o == '-m':
            QUERY = 1
        elif o in ("-s", "--search"):
            searchname = a
        elif o == 'h':
            USAGE()
            sys.exit(0)
        else:
            assert False, "unhandled option"
    if searchname == '':
        searchname = sys.argv[-1]
    main(searchname, QUERY)
