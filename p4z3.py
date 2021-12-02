import z3
from z3 import Int, And, Or, Not, Implies, Solver

#header parser
src_addr = Int('src_addr') 
dst_addr = Int('dst_addr') 
eth_type = Int('eth_type')

src_addr_out = Int('src_addr_out') 
dst_addr_out = Int('dst_addr_out') 
eth_type_out = Int('eth_type_out')


#action
def ingress_YuhlH(src_addr, dst_addr, src_addr_out, dst_addr_out):
    return And(src_addr_out == (dst_addr + 1), dst_addr_out == dst_addr)

def no_action(src_addr, dst_addr, src_addr_out, dst_addr_out):
    return And(src_addr_out == src_addr, dst_addr_out == dst_addr)

#table: defined by controller
def match_table(src_addr, dst_addr, src_addr_out, dst_addr_out):
    p = And(src_addr < 1, ingress_YuhlH(src_addr, dst_addr, src_addr_out, dst_addr_out))
    q = And(src_addr > 0, no_action(src_addr, dst_addr, src_addr_out, dst_addr_out))
    return Or(p, q)

bound = And(And(src_addr>=0, dst_addr>=0), And(src_addr_out>=0, dst_addr_out>=0))

#pipeline
program = And(bound, match_table(src_addr, dst_addr, src_addr_out, dst_addr_out))

# check src_addr_out > 0
inv = (src_addr_out < 1)

s = Solver()
s.add(And(program, inv))  # Check unsat of negation for checking validity
result = s.check()
if result == z3.sat:
    print("Given formula is not valid.")
    print("Counter example: \n", s.model())
elif result == z3.unsat:
    print("Given formula is valid.")
else:  # result == z3.unknown
    print("Inconclusive. Z3 cannot solve with given options.")

