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
bigoh.lineWidth = 1.0


######################################################################
# Main
######################################################################

ctx, surface = bigoh.makeCairoContext()

firstHeight = 150
bigoh.drawTimeGraph(3, ctx, bigoh.centeredRect(top=10, height=firstHeight, horizInset=10))
bigoh.drawTimeGraph(4, ctx, bigoh.centeredRect(top=(firstHeight + 40), height=80, horizInset=10))

surface.write_to_png('img1.png')

