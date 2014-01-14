# antisort_example3.py
#
# Draw a data flow diagram of a mergesort on an
# antisorted input.
#

import bigoh
import math

# Major parameters.
if False:
  numBars = 4
  graphMarginX = 80  # May slightly increase.
  graphMarginY = 60
  barMarginPerc = 0.2
  bigoh.width = 600
  bigoh.height = 400
if True:
  numBars = 8
  graphMarginX = 50  # May slightly increase.
  graphMarginY = 30
  barMarginPerc = 0.3
  bigoh.width = 690
  bigoh.height = 500

ctx, surface = bigoh.makeCairoContext()

# Colors.
maroon = (0.52, 0.14, 0.23)
orange = (0.90, 0.45, 0.21)
grayLevel = 0.9
gray = (grayLevel, grayLevel, grayLevel)

colors = [(0.87, 0.25, 0.40), (0.92, 0.53, 0.24), (0.96, 0.66, 0.35), (0.93, 0.74, 0.28),
          (0.73, 0.69, 0.25), (0.39, 0.51, 0.19), (0.22, 0.39, 0.54), (0.72, 0.23, 0.56)]

# Graph and layout parameters.
#
# Main box parameters:
#  graphMarginX, graphMarginY
#  graphSizeY [graphSizeX depends on which graph it is]
#
# Main within-graph parameters:
#  barX, barMarginX
# 
lgN = int(math.log(numBars) / math.log(2))  # Rounding error seems possible.
numCols = 2 * lgN + 1
totalBars = 5 * numBars - 4
totalBarMargins = totalBars - numCols
roomForGraphsX = bigoh.width - graphMarginX * (numCols - 1)
barX = int(math.floor(roomForGraphsX / (totalBars + barMarginPerc * totalBarMargins)))
print('barX=%d' % barX)
barMarginX = int(barMarginPerc * barX)
print('barMarginX=%d' % barMarginX)
barMarginPerc = barMarginX / float(barX)
roomForGraphMargins = bigoh.width - barX * totalBars - barMarginX * totalBarMargins
graphMarginX = int(roomForGraphMargins / (numCols - 1))
options = {'barMarginPerc': barMarginPerc, 'forcedBarWidth': barX}
roomForGraphsY = bigoh.height - (numBars - 1) * graphMarginY
graphSizeY = int(roomForGraphsY / numBars)


# Functions.

# Expects col to be in [0, 2 * numBars].
def numBarsInCol(col):
  if col == 0: return numBars
  if col <= lgN: return 2 * (numBars / 2 ** col)
  # Otherwise, col is in [numBars + 1, 2 * numBars].
  x = 2 * lgN - col
  return numBars / 2 ** x

def numRowsInCol(col):
  if col <= lgN: return 2 ** col
  x = 2 * lgN - col
  return 2 ** x

def graphBox(col, row):
  centerY = bigoh.height / 2.0
  n = numBarsInCol(col)
  width = barX * n + barMarginX * (n - 1)
  if col == 0:
    top = int(centerY - graphSizeY / 2.0)
    return {'left': 0, 'top': top, 'width': width, 'height': graphSizeY}
  leftBox = graphBox(col - 1, 0)
  left = leftBox['left'] + leftBox['width'] + graphMarginX
  numRows = numRowsInCol(col)
  roomForMargins = bigoh.height - graphSizeY * numRows
  graphMarginY = roomForMargins / (numRows + 1)
  colHeight = numRows * graphSizeY + (numRows - 1) * graphMarginY
  colTop = int(centerY - colHeight / 2.0)
  top = colTop + (graphSizeY + graphMarginY) * row
  return {'left': left, 'top': top, 'width': width, 'height': graphSizeY}

def boxCenter(box):
  return box['left'] + box['width'] / 2.0, box['top'] + box['height'] / 2.0

# Takes a left-to-right line (x1, y1) -> (x2, y2), and
# shrinks it if necessary so that x1 >= xleft and x2 <= xRight.
# Expects x1 < x2.
def restrictLine(x1, y1, x2, y2, xLeft, xRight):
  m = (y2 - y1) / (x2 - x1)
  if x1 < xLeft:
    y1 += m * (xLeft - x1)
    x1 = xLeft
  if x2 > xRight:
    y2 -= m * (x2 - xRight)
    x2 = xRight
  return x1, y1, x2, y2

def drawLine(col1, row1, col2, row2):
  margin = 15
  ctx.set_source_rgb(*gray)
  box1 = graphBox(col1, row1)
  box2 = graphBox(col2, row2)
  x1, y1 = boxCenter(box1)
  x2, y2 = boxCenter(box2)
  xLeft = box1['left'] + box1['width'] + margin
  xRight = box2['left'] - margin
  x1, y1, x2, y2 = restrictLine(x1, y1, x2, y2, xLeft, xRight)
  ctx.move_to(x1, y1)
  ctx.line_to(x2, y2)
  ctx.stroke()

# We expect activeHalf to be a list of indexes into barHeights.
def drawGraphAndKids(barHeights, activeHalf, col, row):
  box = graphBox(col, row)
  barColors = [colors[barHeights[i] - 1] if i in activeHalf else gray for i in range(len(barHeights))]
  #barColors = [orange if i in activeHalf else gray for i in range(len(barHeights))]
  bigoh.drawBarGraph(barHeights, numBars, ctx, box, barColors, **options)
  if len(barHeights) == 2: return  # No kids; we've reached the center column.
  # Left child.
  barHeights = [barHeights[i] for i in activeHalf]
  n = len(barHeights)
  mid = n / 2
  activeHalf = range(mid)
  drawLine(col, row, col + 1, row * 2)
  drawGraphAndKids(barHeights, activeHalf, col + 1, row * 2)
  # Right child.
  activeHalf = range(mid, n)
  drawLine(col, row, col + 1, row * 2 + 1)
  drawGraphAndKids(barHeights, activeHalf, col + 1, row * 2 + 1)
  # Reflected version.
  otherCol = 2 * lgN - col
  box = graphBox(otherCol, row)
  #barColors = [orange for i in range(n)]
  barHeights = sorted(barHeights)
  barColors = [colors[barHeights[i] - 1] for i in range(n)]
  bigoh.drawBarGraph(barHeights, numBars, ctx, box, barColors, **options)
  drawLine(otherCol - 1, 2 * row, otherCol, row)
  drawLine(otherCol - 1, 2 * row + 1, otherCol, row)

def antisorted(arr, stackLimit=-1):
  if stackLimit == 0: return arr
  if len(arr) < 2: return arr
  sortedarr = sorted(arr)
  i = 0 
  left, right = [], []
  while True:
    right.append(sortedarr[i])
    i += 1
    if i == len(arr): break
    left.append(sortedarr[i])
    i += 1
    if i == len(arr): break
  return antisorted(left, stackLimit - 1) + antisorted(right, stackLimit - 1)

arr = antisorted(range(1, numBars + 1))
indexes = range(numBars)
drawGraphAndKids(arr, indexes, 0, 0)

surface.write_to_png('antisort_example3.png')

