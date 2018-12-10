# -*- coding: utf-8 -*-
import os
import sys
from gedcom import Gedcom
from gedcom_families import GedcomFamilies

if len(sys.argv) < 2:
    print('Usage: ./test2.py <file.ged> <last_names>')
    sys.exit(1)

ged_file_path = sys.argv[1]
last_names = []
try:
    last_names = sys.argv[2].split(',')
except:
    pass

gedcomFamilies = GedcomFamilies(ged_file_path)
print(gedcomFamilies.get_dot_graph())


"""
gedcom = Gedcom(ged_file_path)


for element in families:
    print(u'\t_%s [label="%s",height=.1,width=.1];' % (element.get_pointer().replace('@', ''), 'M'))

# ...

# ...

for family in families:
    



    print(u'\tsubgraph cluster_%s {' % family.get_pointer().replace('@', ''))
    print(u'\t\t_%s' % family.get_pointer().replace('@', ''))
    

    # ..

    print(u'\t}')

"""

"""
# cluster for last names
for last_name in last_names:
    print(u'\tsubgraph cluster_%s {' % last_name)
    print(u'\tcolor = blue;')
    for person in individuals:
        (first, last) = person.get_name()
        if last == last_name:
            print(u'\t\t_%s' % person.get_pointer().replace('@', ''))
    print(u'\t}')
"""

print('}')