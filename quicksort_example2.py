import bigoh

# Functions.
def drawBottomBorder(ctx, box):
  ctx.set_source_rgb(0, 0, 0)
  y = box['top'] + box['height']
  ctx.move_to(box['left'], y)
  ctx.line_to(box['left'] + box['width'], y)
  ctx.stroke()

bigoh.width = 600
bigoh.height = 120
ctx, surface = bigoh.makeCairoContext()

# Define colors and dimensions.
maroon = (0.52, 0.14, 0.23)
orange = (0.90, 0.45, 0.21)
gray = (0.80, 0.80, 0.80)
xMargin = 40
widthDelta = 30
options = {'barMarginPerc': 0.6, 'forcedBarWidth': 16}
box = {'top': 10, 'left': 10, 'width': 135, 'height': 90}

barColors = [
    [orange, maroon, maroon, maroon, maroon, maroon],
    [orange, maroon, maroon, None, gray, None, orange, maroon],
    [maroon, None, gray, None, maroon, None, gray, None, maroon, None, gray]
]
barHeights = [
    [4, 6, 2, 3, 5, 1],
    [2, 3, 1, None, 4, None, 6, 5],
    [1, None, 2, None, 3, None, 4, None, 5, None, 6]
]

for i in range(3):
  bigoh.drawBarGraph(barHeights[i], 6, ctx, box, barColors[i], **options)
  drawBottomBorder(ctx, box)
  box['left'] += (box['width'] + xMargin)
  box['width'] += widthDelta

surface.write_to_png('quicksort_example2.png')

