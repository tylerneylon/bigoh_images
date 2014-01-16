#!/usr/bin/python
#
# quicksort_example3.py
#
# Graphs illustrating how quicksort operates
# on an already-sorted import [1, 2, .., 6].
#

import bigoh

# Functions.
def draw_bottom_border(ctx, box):
  ctx.set_source_rgb(0, 0, 0)
  y = box['top'] + box['height']
  ctx.move_to(box['left'], y)
  ctx.line_to(box['left'] + box['width'], y)
  ctx.stroke()

bigoh.width = 130
bigoh.height = 450
ctx, surface = bigoh.make_cairo_context()

# Define colors and dimensions.
maroon = (0.52, 0.14, 0.23)
orange = (0.90, 0.45, 0.21)
gray = (0.80, 0.80, 0.80)
vert_margin = 50
width_delta = 10
options = {'bar_margin_perc': 0.6, 'forced_bar_width': 10}
box = {'top': 10, 'left': 10 + width_delta * 1.5, 'width': 80, 'height': 70}

bar_colors = [
    [orange, maroon, maroon, maroon, maroon, maroon],
    [gray, None, orange, maroon, maroon, maroon, maroon],
    [gray, None, gray, None, orange, maroon, maroon, maroon],
    [gray, None, gray, None, gray, None, orange, maroon, maroon]
]
bar_heights = [
    [1, 2, 3, 4, 5, 6],
    [1, None, 2, 3, 4, 5, 6],
    [1, None, 2, None, 3, 4, 5, 6],
    [1, None, 2, None, 3, None, 4, 5, 6]
]

for i in range(4):
  bigoh.draw_bar_graph(bar_heights[i], 6, ctx, box, bar_colors[i], **options)
  draw_bottom_border(ctx, box)
  box['top'] += (box['height'] + vert_margin)
  box['left'] -= (width_delta / 2)
  box['width'] += width_delta

surface.write_to_png('quicksort_example3.png')

