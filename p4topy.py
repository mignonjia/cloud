import numpy as np
import json

headers = {}

filein = 'test2.json'
fileout = 'out.py'

with open(filein, 'r') as jsonfile:
    json_string = json.load(jsonfile)

ret = open(fileout, 'w')
ret.write('import z3\n')
ret.write('from z3 import Int, And, Or, Not, Implies, Solver\n\n')
ret.write('s = Solver()\n\n')
ret.write('#Define Variabiles\n')

for item in json_string['header_types']:
    if item['name'] == 'scalars_0' or item['name'] == 'standard_metadata':
        continue
    headers[item['name']] = item['fields']

tables = []
# get the number of match-action tables
for item in json_string['pipelines']:
    if item['name'] != 'ingress':
        continue
    for table in item['tables']:
        tables.append(table)

num_table = len(tables)
num_var = num_table + 1

vars = []

for item in json_string['headers']:
    header_type = item['header_type']
    if header_type == 'scalars_0' or header_type == 'standard_metadata':
        continue
    for name, bit, stat in headers[header_type]:            
        ret.write(name + ' = [ Int(\'' + name + '%s\' % i) for i in range(' + str(num_var) +') ]\n')
        vars.append(name)
        for i in range(num_var):
            thisvar = name + '[' + str(i) + ']'
            ret.write('s.add(' + thisvar + ' >= 0)\n')
            ret.write('s.add(' + thisvar + ' <= 0x' + '1'*bit + ')\n')

ret.write('\n#action\n')
for action in json_string['actions']:
    ret.write('def ' + action['name'][:3] + '(')
    for i in range(len(vars)-1):
         ret.write(vars[i] + ', ')
    ret.write(vars[-1] + '):\n')

    if action['name'] == 'NoAction':
        ret.write('    p = (' + vars[0] +'[1] == ' + vars[0] + '[0])\n')
        ret.write('    q = (' + vars[1] +'[1] == ' + vars[1] + '[0])\n')
        ret.write('    return And(p,q)\n\n')

    for item in action['primitives']:
        if item['op'] == 'assign':
                # too strict!!!
            left = item['parameters'][0]['value'][1]
            right = item['parameters'][1]['value'][1] 
            ret.write('    p = (' + left +'[1] == ' + right + '[0])\n')
            ret.write('    q = (' + right +'[1] == ' + right + '[0])\n')
            ret.write('    return And(p,q)\n\n')

ret.write('#table\n')
for table in tables:
    ret.write('def table(' )
    for i in range(len(vars)-1):
        ret.write(vars[i] + ', ')
    ret.write(vars[-1] + '):\n')
    ret.write('    #define control table\n')
    ret.write('    return 1\n\n')

ret.write('#pipeline\n')
ret.write('program = table(')
for i in range(len(vars)-1):
    ret.write(vars[i] + ', ')
ret.write(vars[-1] + ')\n\n')

ret.write('#define your invariant')

