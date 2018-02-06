#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:55:16 2018

@author: craig
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

OSMFILE = "sydney_sample.osm"
postal_type_re = re.compile('(?<!\d)\d{4}(?!\d)')     #Identifies postal codes four digits in length. 

def audit_postal_code(postal_types, postal_code):     
    m = postal_type_re.search(postal_code) 
    if m:                                        
        postal_type = m.group()                       #Take postal codes four digits in length, groups them, sets them equal to postal_type.
        postal_types[postal_type].add(postal_code)    #Add postal codes to the postal types dictionary.  
    
               
def audit_file(OSMFILE):
    open(OSMFILE, "r")
    postal_types = defaultdict(set)
    for event, elem in ET.iterparse(OSMFILE, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == 'addr:postcode':
                    audit_postal_code(postal_types, tag.attrib['v'])
                    
    return postal_types   

audit_file(OSMFILE)