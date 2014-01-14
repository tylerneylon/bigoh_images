# quicksort_example3.py
#
# Graphs illustrating how quicksort operates
# on an already-sorted import [1, 2, .., 6].
#

import bigoh

# Functions.
def drawBottomBorder(ctx, box):
  ctx.set_source_rgb(0, 0, 0)
  y = box['top'] + box['height']
  ctx.move_to(box['left'], y)
  ctx.line_to(box['left'] + box['width'], y)
  ctx.stroke()

bigoh.width = 200
bigoh.height = 450
ctx, surface = bigoh.makeCairoContext()

# Define colors and dimensions.
maroon = (0.52, 0.14, 0.23)
orange = (0.90, 0.45, 0.21)
gray = (0.80, 0.80, 0.80)
vertMargin = 50
widthDelta = 10
options = {'barMarginPerc': 0.6, 'forcedBarWidth': 10}
box = {'top': 10, 'left': 10 + widthDelta * 1.5, 'width': 80, 'height': 70}

barColors = [
    [orange, maroon, maroon, maroon, maroon, maroon],
    [gray, None, orange, maroon, maroon, maroon, maroon],
    [gray, None, gray, None, orange, maroon, maroon, maroon],
    [gray, None, gray, None, gray, None, orange, maroon, maroon]
]
barHeights = [
    [1, 2, 3, 4, 5, 6],
    [1, None, 2, 3, 4, 5, 6],
    [1, None, 2, None, 3, 4, 5, 6],
    [1, None, 2, None, 3, None, 4, 5, 6]
]

for i in range(4):
  bigoh.drawBarGraph(barHeights[i], 6, ctx, box, barColors[i], **options)
  drawBottomBorder(ctx, box)
  box['top'] += (box['height'] + vertMargin)
  box['left'] -= (widthDelta / 2)
  box['width'] += widthDelta

surface.write_to_png('quicksort_example3.png')

