# antisort_example1.py
#
# Draw graphs to illustrate the antisort function.
#

import bigoh

bigoh.width = 513
bigoh.height = 110
ctx, surface = bigoh.makeCairoContext()

# Define colors and dimensions.
maroon = (0.52, 0.14, 0.23)
orange = (0.90, 0.45, 0.21)
numBars = 9
options = {'barMarginPerc': 0.0}
barWidth = 17
box = {'top': 10, 'left': 10, 'width': barWidth * numBars, 'height': 90}


# Functions.
def alternatingColors(numBars):
  global maroon, orange
  return [orange if i % 2 else maroon for i in range(numBars)]


# Main.

# Draw the sorted graph with alternating colors.
barHeights = range(1, numBars + 1)
barColors = alternatingColors(numBars)
bigoh.drawBarGraph(barHeights, numBars, ctx, box, barColors, **options)

# Draw left in orange with heights 2, 4, etc.
barHeights = range(2, numBars + 1, 2)
barColors = [orange for i in barHeights]
box['left'] = 350
box['width'] = barWidth * len(barHeights)
bigoh.drawBarGraph(barHeights, numBars, ctx, box, barColors, **options)

# Draw right in maroon with heights 1, 3, etc.
barHeights = range(1, numBars + 1, 2)
barColors = [maroon for i in barHeights]
box['left'] += box['width']
box['width'] = barWidth * len(barHeights)
bigoh.drawBarGraph(barHeights, numBars, ctx, box, barColors, **options)


surface.write_to_png('antisort_example1.png')
