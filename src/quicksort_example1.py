#!/usr/bin/python

import bigoh

# Functions.
def draw_bottom_border(ctx, box):
  ctx.set_source_rgb(0, 0, 0)
  y = box['top'] + box['height']
  ctx.move_to(box['left'], y)
  ctx.line_to(box['left'] + box['width'], y)
  ctx.stroke()

ctx, surface = bigoh.make_cairo_context()

# Define colors and dimensions.
maroon = (0.52, 0.14, 0.23)
orange = (0.90, 0.45, 0.21)
gray = (0.80, 0.80, 0.80)
vert_margin = 60
width_delta = 60
options = {'bar_margin_perc': 0.6, 'forced_bar_width': 35}
box = {'top': 10, 'left': 10 + width_delta, 'width': 280, 'height': 160}

bar_colors = [
    [orange, maroon, maroon, maroon, maroon, maroon],
    [orange, maroon, maroon, None, gray, None, orange, maroon],
    [maroon, None, gray, None, maroon, None, gray, None, maroon, None, gray]
]
bar_heights = [
    [4, 6, 2, 3, 5, 1],
    [2, 3, 1, None, 4, None, 6, 5],
    [1, None, 2, None, 3, None, 4, None, 5, None, 6]
]

for i in range(3):
  bigoh.draw_bar_graph(bar_heights[i], 6, ctx, box, bar_colors[i], **options)
  draw_bottom_border(ctx, box)
  box['top'] += (box['height'] + vert_margin)
  box['left'] -= (width_delta / 2)
  box['width'] += width_delta

surface.write_to_png('quicksort_example1.png')

