#!/usr/bin/python
#
# t_n_tables.py
#
# Generate {quicksort,mergesort}_t_n.txt
# with tabular data that may be imported into
# the Grapher app.
#

import math

def quicksort_t_n(n):
  return n * (n - 1) / 2

def mergesort_t_n(n):
  k = math.ceil(math.log(n) / math.log(2))
  return n * k - 2 ** k + 1

def write_table_for_fn(fn):
  filename = fn.func_name + '.txt'
  writer = open(filename, 'w')
  for n in range(1, 20):
    time = fn(n)
    writer.write('%d,%d,%d\n' % (n, time, n))
  writer.close()

for t_n in [quicksort_t_n, mergesort_t_n]:
  write_table_for_fn(t_n)
