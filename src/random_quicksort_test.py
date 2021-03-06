#!/usr/bin/python
#
# random_quicksort_test.py
#
# Test that randomized quicksort does indeed sort correctly, and
# using running time that appears to be independent of the input ordering.
# 

import bigoh

num_trials = 10000
test_arrays = [
      [1, 2, 3, 4, 5, 6],
      [3, 2, 6, 4, 1, 5],
      [6, 1, 5, 2, 4, 3]
    ]

for arr in test_arrays:
  num_compares = 0
  print('\n_testing input %s' % `arr`)
  result = bigoh.randomized_quicksorted(arr)
  print('output=%s' % `result`)
  for i in range(num_trials):
    num_compares += bigoh.calc_num_compares(arr, bigoh.randomized_quicksorted)
  avg_num_compares = num_compares / float(num_trials)
  print('after %d trials, avg #comparisons=%.1f' % (num_trials, avg_num_compares))

