#!/usr/bin/python
#
# antisort.py
#
# Test that the antisorting function achieves the
# expected maximum number of comparisons.
#

import bigoh
import math

# Rearrange the elements of an array in order to
# maximize the time required by mergesort; expects
# the elements to be unique.
def antisorted(arr):
  if len(arr) < 2: return arr
  sortedarr = sorted(arr)
  i = 0
  left, right = [], []
  while True:
    right.append(sortedarr[i])
    i += 1
    if i == len(arr): break
    left.append(sortedarr[i])
    i += 1
    if i == len(arr): break
  return antisorted(left) + antisorted(right)


def mergesort_recursive_t_n(n):
  if n < 2: return 0
  small_half = math.floor(n / 2.0)
  big_half = math.ceil(n / 2.0)
  return (n - 1 + mergesort_recursive_t_n(small_half) +
                 mergesort_recursive_t_n(big_half))

def mergesort_explicit_t_n(n):
  k = math.ceil(math.log(n) / math.log(2))
  return n * k - 2 ** k + 1

def mergesort_on_antisorted(n):
  arr = range(1, n + 1)
  arr = antisorted(arr)
  return bigoh.calc_num_compares(arr, bigoh.mergesorted)


for n in range(1, 20):
  print('\n\nn=%d' % n)
  print('recursively computed time = %d' % mergesort_recursive_t_n(n))
  print('explicitly computed time  = %d' % mergesort_explicit_t_n(n))
  print('time required on antisort = %d' % mergesort_on_antisorted(n))
  print('antisorted array = %s' % `antisorted(range(1, n + 1))`)
