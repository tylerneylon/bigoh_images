#!/usr/bin/python
#
# antisort_example3.py
#
# Draw a data flow diagram of a mergesort on an
# antisorted input.
#

import bigoh
import math

# Major parameters.
if False:
  num_bars = 4
  graph_margin_x = 80  # May slightly increase.
  graph_margin_y = 60
  bar_margin_perc = 0.2
  bigoh.width = 600
  bigoh.height = 400
if True:
  num_bars = 8
  graph_margin_x = 50  # May slightly increase.
  graph_margin_y = 30
  bar_margin_perc = 0.3
  bigoh.width = 690
  bigoh.height = 500

ctx, surface = bigoh.make_cairo_context()

# Colors.
maroon = (0.52, 0.14, 0.23)
orange = (0.90, 0.45, 0.21)
gray_level = 0.9
gray = (gray_level, gray_level, gray_level)

colors = [(0.87, 0.25, 0.40), (0.92, 0.53, 0.24), (0.96, 0.66, 0.35), (0.93, 0.74, 0.28),
          (0.73, 0.69, 0.25), (0.39, 0.51, 0.19), (0.22, 0.39, 0.54), (0.72, 0.23, 0.56)]

# Graph and layout parameters.
#
# Main box parameters:
#  graph_margin_x, graph_margin_y
#  graph_size_y [graph_size_x depends on which graph it is]
#
# Main within-graph parameters:
#  bar_x, bar_margin_x
# 
lg_n = int(math.log(num_bars) / math.log(2))  # Rounding error seems possible.
num_cols = 2 * lg_n + 1
total_bars = 5 * num_bars - 4
total_bar_margins = total_bars - num_cols
room_for_graphs_x = bigoh.width - graph_margin_x * (num_cols - 1)
bar_x = int(math.floor(room_for_graphs_x / (total_bars + bar_margin_perc * total_bar_margins)))
print('bar_x=%d' % bar_x)
bar_margin_x = int(bar_margin_perc * bar_x)
print('bar_margin_x=%d' % bar_margin_x)
bar_margin_perc = bar_margin_x / float(bar_x)
room_for_graph_margins = bigoh.width - bar_x * total_bars - bar_margin_x * total_bar_margins
graph_margin_x = int(room_for_graph_margins / (num_cols - 1))
options = {'bar_margin_perc': bar_margin_perc, 'forced_bar_width': bar_x}
room_for_graphs_y = bigoh.height - (num_bars - 1) * graph_margin_y
graph_size_y = int(room_for_graphs_y / num_bars)


# Functions.

# Expects col to be in [0, 2 * num_bars].
def num_bars_in_col(col):
  if col == 0: return num_bars
  if col <= lg_n: return 2 * (num_bars / 2 ** col)
  # Otherwise, col is in [num_bars + 1, 2 * num_bars].
  x = 2 * lg_n - col
  return num_bars / 2 ** x

def num_rowsInCol(col):
  if col <= lg_n: return 2 ** col
  x = 2 * lg_n - col
  return 2 ** x

def graph_box(col, row):
  center_y = bigoh.height / 2.0
  n = num_bars_in_col(col)
  width = bar_x * n + bar_margin_x * (n - 1)
  if col == 0:
    top = int(center_y - graph_size_y / 2.0)
    return {'left': 0, 'top': top, 'width': width, 'height': graph_size_y}
  left_box = graph_box(col - 1, 0)
  left = left_box['left'] + left_box['width'] + graph_margin_x
  num_rows = num_rowsInCol(col)
  room_for_margins = bigoh.height - graph_size_y * num_rows
  graph_margin_y = room_for_margins / (num_rows + 1)
  col_height = num_rows * graph_size_y + (num_rows - 1) * graph_margin_y
  col_top = int(center_y - col_height / 2.0)
  top = col_top + (graph_size_y + graph_margin_y) * row
  return {'left': left, 'top': top, 'width': width, 'height': graph_size_y}

def box_center(box):
  return box['left'] + box['width'] / 2.0, box['top'] + box['height'] / 2.0

# Takes a left-to-right line (x1, y1) -> (x2, y2), and
# shrinks it if necessary so that x1 >= xleft and x2 <= x_right.
# Expects x1 < x2.
def restrict_line(x1, y1, x2, y2, x_left, x_right):
  m = (y2 - y1) / (x2 - x1)
  if x1 < x_left:
    y1 += m * (x_left - x1)
    x1 = x_left
  if x2 > x_right:
    y2 -= m * (x2 - x_right)
    x2 = x_right
  return x1, y1, x2, y2

def draw_line(col1, row1, col2, row2):
  margin = 15
  ctx.set_source_rgb(*gray)
  box1 = graph_box(col1, row1)
  box2 = graph_box(col2, row2)
  x1, y1 = box_center(box1)
  x2, y2 = box_center(box2)
  x_left = box1['left'] + box1['width'] + margin
  x_right = box2['left'] - margin
  x1, y1, x2, y2 = restrict_line(x1, y1, x2, y2, x_left, x_right)
  ctx.move_to(x1, y1)
  ctx.line_to(x2, y2)
  ctx.stroke()

# We expect active_half to be a list of indexes into bar_heights.
def draw_graph_and_kids(bar_heights, active_half, col, row):
  box = graph_box(col, row)
  bar_colors = [colors[bar_heights[i] - 1] if i in active_half else gray for i in range(len(bar_heights))]
  #bar_colors = [orange if i in active_half else gray for i in range(len(bar_heights))]
  bigoh.draw_bar_graph(bar_heights, num_bars, ctx, box, bar_colors, **options)
  if len(bar_heights) == 2: return  # No kids; we've reached the center column.
  # Left child.
  bar_heights = [bar_heights[i] for i in active_half]
  n = len(bar_heights)
  mid = n / 2
  active_half = range(mid)
  draw_line(col, row, col + 1, row * 2)
  draw_graph_and_kids(bar_heights, active_half, col + 1, row * 2)
  # Right child.
  active_half = range(mid, n)
  draw_line(col, row, col + 1, row * 2 + 1)
  draw_graph_and_kids(bar_heights, active_half, col + 1, row * 2 + 1)
  # Reflected version.
  other_col = 2 * lg_n - col
  box = graph_box(other_col, row)
  #bar_colors = [orange for i in range(n)]
  bar_heights = sorted(bar_heights)
  bar_colors = [colors[bar_heights[i] - 1] for i in range(n)]
  bigoh.draw_bar_graph(bar_heights, num_bars, ctx, box, bar_colors, **options)
  draw_line(other_col - 1, 2 * row, other_col, row)
  draw_line(other_col - 1, 2 * row + 1, other_col, row)

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

arr = antisorted(range(1, num_bars + 1))
indexes = range(num_bars)
draw_graph_and_kids(arr, indexes, 0, 0)

surface.write_to_png('antisort_example3.png')

