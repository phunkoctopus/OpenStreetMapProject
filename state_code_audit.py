#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 14:50:54 2018

@author: craig
"""

#Auditing state codes, with the expected 3-letter value as NSW for New South Wales.
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

s_file = "sydney_australia.osm"
state_type_re = re.compile('(?<!\d)\d{3}(?!\d)')

def audit_state_code (state_types, state_code):
    m = state_type_re.search(state_code)
    if m:
        state_type = m.group()
        state_types[state_type].add(state_code)
        
def is_state_code(elem):
    return (elem.attrib['k'] == "addr:state")

def sc_audit(s_file):
    open(s_file, "r")
    state_types = defaultdict(set)
    for event, elem in ET.iterparse(s_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_state_code(tag):
                    audit_state_code(state_types, tag.attrib['v'])
    
    return state_types
