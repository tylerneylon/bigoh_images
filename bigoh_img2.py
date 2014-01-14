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
bigoh.lineWidth = 1.0


ctx, surface = bigoh.makeCairoContext()
# TEMP TODO The end of the range should be 11. I'm using 8 for faster testing.
for n in range(3, 8):  # Real image should go up to 10 (so end=11).
  #print('n=%d' % n)
  #barHeights, perms = bigoh.getRuntimesForSorting(n)
  #bigoh.drawBarGraph(n, ctx, bigoh.centeredRect(top=10 + (n - 3) * 100, height=100, horizInset=10))
  box = bigoh.centeredRect(top=10 + (n - 3) * 100, height=100, horizInset=10)
  bigoh.drawTimeGraph(n, ctx, box, drawPerms=False, sortTimes=True)
surface.write_to_png('img2.png')

