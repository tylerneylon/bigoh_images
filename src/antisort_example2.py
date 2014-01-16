#!/usr/bin/python
#
# antisort_example2.py
#
# Draw graphs to show how the antisort function
# works step-by-step.
#

import bigoh
import math

num_bars = 64
bigoh.width = 700
bigoh.height = num_bars + 20
ctx, surface = bigoh.make_cairo_context()

# Define colors and dimensions.
maroon = (0.52, 0.14, 0.23)
orange = (0.90, 0.45, 0.21)
options = {'bar_margin_perc': 0.0}
bar_width = 17
box = {'top': 10, 'left': 10, 'width': bar_width * num_bars, 'height': num_bars}
graph_margin = 1


# Functions.

# Expects n to be a positive integer; returns postive integer m
# such that m is a multiple of n, m <= x, and m + n > x.
def floor_to_multiple_of(x, n):
  return int(math.floor(x / n) * n)

def alternating_colors(num_bars):
  global maroon, orange
  return [orange if i % 2 else maroon for i in range(num_bars)]

def antisorted(arr, stack_limit=-1):
  if stack_limit == 0: return arr
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
  return antisorted(left, stack_limit - 1) + antisorted(right, stack_limit - 1)


# Main.

# Find out how many graphs we'll need to draw, and the related graph dimensions.
num_graphs = int(math.ceil(math.log(num_bars) / math.log(2.0)) + 1)
print('num_graphs=%d' % num_graphs)
max_graph_width = math.floor((bigoh.width - 20 - (num_graphs - 1) * graph_margin) / num_graphs)
print('max_graph_width=%d' % max_graph_width)
graph_width = floor_to_multiple_of(max_graph_width, num_bars)
print('graph_width=%d' % graph_width)
lost_pixels = (max_graph_width - graph_width) * num_graphs
graph_margin += int(lost_pixels / (num_graphs - 1))
box['width'] = graph_width
bar_width = graph_width / num_bars

# Draw the graphs.
for i in range(num_graphs):
  arr = range(1, num_bars + 1)
  arr = antisorted(arr, stack_limit=i)
  bar_colors = [orange for j in arr]
  bigoh.draw_bar_graph(arr, num_bars, ctx, box, bar_colors, **options)
  box['left'] += (box['width'] + graph_margin)

surface.write_to_png('antisort_example2.png')
