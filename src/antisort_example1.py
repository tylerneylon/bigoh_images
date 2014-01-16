#!/usr/bin/python
#
# antisort_example1.py
#
# Draw graphs to illustrate the first step of
# the antisort function.
#

import bigoh

bigoh.width = 513
bigoh.height = 110
ctx, surface = bigoh.make_cairo_context()

# Define colors and dimensions.
maroon = (0.52, 0.14, 0.23)
orange = (0.90, 0.45, 0.21)
num_bars = 9
options = {'bar_margin_perc': 0.0}
bar_width = 17
box = {'top': 10, 'left': 10, 'width': bar_width * num_bars, 'height': 90}


# Functions.
def alternating_colors(num_bars):
  global maroon, orange
  return [orange if i % 2 else maroon for i in range(num_bars)]


# Main.

# Draw the sorted graph with alternating colors.
bar_heights = range(1, num_bars + 1)
bar_colors = alternating_colors(num_bars)
bigoh.draw_bar_graph(bar_heights, num_bars, ctx, box, bar_colors, **options)

# Draw left in orange with heights 2, 4, etc.
bar_heights = range(2, num_bars + 1, 2)
bar_colors = [orange for i in bar_heights]
box['left'] = 350
box['width'] = bar_width * len(bar_heights)
bigoh.draw_bar_graph(bar_heights, num_bars, ctx, box, bar_colors, **options)

# Draw right in maroon with heights 1, 3, etc.
bar_heights = range(1, num_bars + 1, 2)
bar_colors = [maroon for i in bar_heights]
box['left'] += box['width']
box['width'] = bar_width * len(bar_heights)
bigoh.draw_bar_graph(bar_heights, num_bars, ctx, box, bar_colors, **options)


surface.write_to_png('antisort_example1.png')
