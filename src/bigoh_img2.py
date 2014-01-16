#!/usr/bin/python
#
# bigoh_img2.py
#
# Make images to visualize the running times of
# quicksort vs mergesort.
#
# The current version produces sorted time complexity bar
# graphs for n=3 through n=10.
#

import bigoh
import cairo

bigoh.width = 896
bigoh.height = 800
bigoh.line_width = 1.0


ctx, surface = bigoh.make_cairo_context()
for n in range(3, 8):  # Real image should go up to 10 (so end=11).
  #print('n=%d' % n)
  #bar_heights, perms = bigoh.get_runtimes_for_sorting(n)
  #bigoh.draw_bar_graph(n, ctx, bigoh.centered_rect(top=10 + (n - 3) * 100, height=100, horiz_inset=10))
  box = bigoh.centered_rect(top=10 + (n - 3) * 100, height=100, horiz_inset=10)
  bigoh.draw_time_graph(n, ctx, box, draw_perms=False, sort_times=True)
surface.write_to_png('quick_vs_merge2.png')

