import numpy as np
import json
import z3
from z3 import Int, And, Or, Not, Implies, Solver

#assume 1 header_type and 1 table

s = Solver()

headers = {}

filein = 'test2.json'
fileout = 'out.py'

with open(filein, 'r') as jsonfile:
    json_string = json.load(jsonfile)

ret = open(fileout, 'w')

for item in json_string['header_types']:
    if item['name'] == 'scalars_0' or item['name'] == 'standard_metadata':
        continue
    headers[item['name']] = item['fields']

print(headers)

tables = []
# get the number of match-action tables
for item in json_string['pipelines']:
    if item['name'] != 'ingress':
        continue
    for table in item['tables']:
        tables.append(table)

num_table = len(tables)
num_var = num_table + 1

print(num_table)
var = []

for item in json_string['headers']:
    header_type = item['header_type']
    if header_type == 'scalars_0' or header_type == 'standard_metadata':
        continue
    X = [[Int("x_%s_%s" % (name, i)) for name, _, _ in headers[header_type]] for i in range(num_var)]

for action in json_string['actions']:
    if action['name'] == 'NoAction':
        1
#print(json_string[''])