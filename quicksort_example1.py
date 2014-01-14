import bigoh

# Functions.
def drawBottomBorder(ctx, box):
  ctx.set_source_rgb(0, 0, 0)
  y = box['top'] + box['height']
  ctx.move_to(box['left'], y)
  ctx.line_to(box['left'] + box['width'], y)
  ctx.stroke()

ctx, surface = bigoh.makeCairoContext()

# Define colors and dimensions.
maroon = (0.52, 0.14, 0.23)
orange = (0.90, 0.45, 0.21)
gray = (0.80, 0.80, 0.80)
vertMargin = 60
widthDelta = 60
options = {'barMarginPerc': 0.6, 'forcedBarWidth': 35}
box = {'top': 10, 'left': 10 + widthDelta, 'width': 280, 'height': 160}

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
  box['top'] += (box['height'] + vertMargin)
  box['left'] -= (widthDelta / 2)
  box['width'] += widthDelta

surface.write_to_png('quicksort_example1.png')

