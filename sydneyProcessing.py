#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:21:54 2018

@author: craig
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
   
#Tag types, a count of each of four tag categories placed in a dictionary

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

                             
def key_type(element, keys):
    if element.tag == "tag":
        print(element.get('k'))
        if lower.search(element.get('k')):
            keys["lower"] += 1
        elif lower_colon.search(element.get('k')):
            keys["lower_colon"] += 1
        elif problemchars.search(element.get('k')):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
            pprint.pprint(keys)
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


def test():
    keys = process_map('sydney_australia.osm')
    pprint.pprint(keys)

    
if __name__ == "__main__":
    test()


    
#Improving Street Names

OSMFILE = "sydney_australia.osm"
street_type_re = re.compile(r'\b\S+\.?$\xf3', re.IGNORECASE)  


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "West", "East", "South", "North", "Way"]

#Correct street name abbreviations and typo (i.e., Mainland St. => Mainland Street, Broadway W => Broadway West, Boundary Rd. => Boundary Road) 
mapping = {"St": "Street",
           "St.": "Street",
           "Rd.": "Road",
           "Ave": "Avenue",
           "west": "West",
           "W": "West",
           "street": "Street",
           "Blvd": "Boulevard",
           "Denmanstreet": "Denman Street"
           }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):    
#making revisions, updating street names
    m = street_type_re.search(name)
    if m.group() not in expected:
        if m.group() in mapping.keys():
            name = re.sub(m.group(), mapping[m.group()], name)
    return name


def test():
    st_types = audit(OSMFILE)

    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()