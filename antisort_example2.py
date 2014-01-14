# antisort_example2.py
#
# Draw graphs to illustrate the antisort function.
#

import bigoh
import math

numBars = 64
bigoh.width = 700
bigoh.height = numBars + 20
ctx, surface = bigoh.makeCairoContext()

# Define colors and dimensions.
maroon = (0.52, 0.14, 0.23)
orange = (0.90, 0.45, 0.21)
options = {'barMarginPerc': 0.0}
barWidth = 17
box = {'top': 10, 'left': 10, 'width': barWidth * numBars, 'height': numBars}
graphMargin = 1


# Functions.

# Expects n to be a positive integer; returns postive integer m
# such that m is a multiple of n, m <= x, and m + n > x.
def floorToMultipleOf(x, n):
  return int(math.floor(x / n) * n)

def alternatingColors(numBars):
  global maroon, orange
  return [orange if i % 2 else maroon for i in range(numBars)]

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


# Main.

# Find out how many graphs we'll need to draw, and the related graph dimensions.
numGraphs = int(math.ceil(math.log(numBars) / math.log(2.0)) + 1)
print('numGraphs=%d' % numGraphs)
maxGraphWidth = math.floor((bigoh.width - 20 - (numGraphs - 1) * graphMargin) / numGraphs)
print('maxGraphWidth=%d' % maxGraphWidth)
graphWidth = floorToMultipleOf(maxGraphWidth, numBars)
print('graphWidth=%d' % graphWidth)
lostPixels = (maxGraphWidth - graphWidth) * numGraphs
graphMargin += int(lostPixels / (numGraphs - 1))
box['width'] = graphWidth
barWidth = graphWidth / numBars

# Draw the graphs.
for i in range(numGraphs):
  arr = range(1, numBars + 1)
  arr = antisorted(arr, stackLimit=i)
  barColors = [orange for j in arr]
  bigoh.drawBarGraph(arr, numBars, ctx, box, barColors, **options)
  box['left'] += (box['width'] + graphMargin)

surface.write_to_png('antisort_example2.png')
