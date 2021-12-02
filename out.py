import z3
from z3 import Int, And, Or, Not, Implies, Solver

s = Solver()

#Define Variabiles
dst_addr = [ Int('dst_addr%s' % i) for i in range(2) ]
s.add(dst_addr[0] >= 0)
s.add(dst_addr[0] < 2**48)
s.add(dst_addr[1] >= 0)
s.add(dst_addr[1] < 2**48)
src_addr = [ Int('src_addr%s' % i) for i in range(2) ]
s.add(src_addr[0] >= 0)
s.add(src_addr[0] < 2**48)
s.add(src_addr[1] >= 0)
s.add(src_addr[1] < 2**48)

#action
def NoA(dst_addr, src_addr):
    p = (dst_addr[1] == dst_addr[0])
    q = (src_addr[1] == src_addr[0])
    return And(p,q)

def ing(dst_addr, src_addr):
    p = (src_addr[1] == dst_addr[0])
    q = (dst_addr[1] == dst_addr[0])
    return And(p,q)

#table
def table(dst_addr, src_addr):
    #define control table
    p = And(src_addr[0] < 1, NoA(dst_addr, src_addr))
    q = And(src_addr[0] >= 1, ing(dst_addr, src_addr)) 
    return Or(p,q)

#pipeline
program = table(dst_addr, src_addr)

#define your invariant
inv = (src_addr[1] < 0)

s.add(And(program, inv))  # Check unsat of negation for checking validity
result = s.check()
if result == z3.sat:
    print("Given formula is not valid.")
    print("Counter example: \n", s.model())
elif result == z3.unsat:
    print("Given formula is valid.")
else:  # result == z3.unknown
    print("Inconclusive. Z3 cannot solve with given options.")