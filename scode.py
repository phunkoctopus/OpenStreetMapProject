#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 19:42:10 2018

@author: craig
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "sydney_australia.osm"
state_type_re = re.compile(r'\b\S+\.?$\xf3', re.IGNORECASE)  


expected = ["NSW"]


def audit_state_type(state_types, state_code):
    m = state_type_re.search(state_code)
    if m:
        state_type = m.group()
        if state_type not in expected:
            state_types[state_type].add(state_code)

def is_state_code(elem):
    return (elem.attrib['k'] == "is_in:state_code")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    state_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_state_code(tag):
                    audit_state_type(state_types, tag.attrib['v'])
    osm_file.close()
    return state_types


def test():
    st_types = audit(OSMFILE)

    pprint.pprint(dict(st_types))
