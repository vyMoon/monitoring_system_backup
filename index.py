import sys, ast
from menu import Menu
# args = [ast.literal_eval(a) for a in sys.argv[1:]]
# print(args)

m = Menu()
m.start(
  [ast.literal_eval(a) for a in sys.argv[1:]]
)

import ast, sys
entity = ast.literal_eval(sys.argv[1])
