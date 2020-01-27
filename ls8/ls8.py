#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU(10000, 8)

cpu.load()
cpu.run()