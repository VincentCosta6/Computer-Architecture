#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU(8, 10000, False)

cpu.load(sys.argv[1])
cpu.run_hot()