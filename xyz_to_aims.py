#!/auto/vestec1-elixir/home/manishkumar/.conda/envs/kpython310/bin/python3.1

import sys
import argparse
from ase.io import read,write
atom=read(sys.argv[1])

if len(sys.argv)<=2:
    write('geometry.in',atom)
else:
    write('inp.xyz',atom)
