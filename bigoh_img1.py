#!/usr/bin/python
#
# bigoh_img1.py
#
# Make images to visualize the running times of
# quicksort vs mergesort.
#

import bigoh
import cairo

# TODO Standardize use of camel-case vs underscores.

bigoh.width = 700
bigoh.height = 280
bigoh.line_width = 1.0


######################################################################
# Main
######################################################################

ctx, surface = bigoh.make_cairo_context()

first_height = 150
bigoh.draw_time_graph(3, ctx, bigoh.centered_rect(top=10, height=first_height, horiz_inset=10))
bigoh.draw_time_graph(4, ctx, bigoh.centered_rect(top=(first_height + 40), height=80, horiz_inset=10))

surface.write_to_png('img1.png')

