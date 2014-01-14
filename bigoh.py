# bigoh.py
#
# Sort-measuring and bar-graph-drawing functions.
#

import cairo

######################################################################
# Globals
######################################################################

numCompares = 0
width = 700
height = 700
lineWidth = 1.0


######################################################################
# Sorting functions
######################################################################

def quicksorted(arr):
  global numCompares
  n = len(arr)
  if n < 2: return arr

  # Find left & right lists so left < pivot <= right.
  pivot, left, right = arr[0], [], []
  for item in arr[1:n]:
    numCompares += 1
    if item < pivot: left.append(item)
    else: right.append(item)
  return quicksorted(left) + [pivot] + quicksorted(right)

def mergesorted(arr):
  global numCompares
  n = len(arr)
  if n < 2: return arr

  # 1. Split in half.
  mid = int(n / 2)
  left = mergesorted(arr[0:mid])
  right = mergesorted(arr[mid:n])

  # 2. Merge together.
  sorted, i, j = [], 0, 0
  while len(sorted) < n:
    numCompares += 1
    if left[i] < right[j]:
      sorted.append(left[i])
      i += 1
    else:
      sorted.append(right[j])
      j += 1
    if i == len(left): sorted += right[j:]
    if j == len(right): sorted += left[i:]
  return sorted

def calcNumCompares(arr, fn):
  global numCompares
  numCompares = 0
  fn(arr)
  return numCompares

# Returns m', value.
def getValWithMod(m, mx):
  return (int(m / mx), m % mx)

# This is Algorithm L in section 7.2.1.2 of Knuth's
# Art of Computer Programming, Volume 4A.
def permsOfLen(n):
  perm = range(1, n + 1)
  yield perm
  while True:
    # Find the right-most i so that perm[i] < perm[i + 1].
    i = n - 2
    while i >= 0 and perm[i] > perm[i + 1]: i -= 1
    if i < 0: return
    # Find the right-most j so that perm[j] > perm[i].
    j = n - 1
    while perm[j] < perm[i]: j -= 1
    perm[i], perm[j] = perm[j], perm[i]
    perm[i + 1:n] = perm[n - 1:i:-1]  # Reverse the list after perm[i].
    yield perm

def permsOfLenAlternative(n):
  i = 0
  while True:
    m = i
    arr = range(1, n + 1)
    for j in range(n):
      m, val = getValWithMod(m, n - j)
      arr[j], arr[val + j] = arr[val + j], arr[j]
    if i > 0 and arr == range(1, n + 1): return
    yield arr
    i += 1


######################################################################
# Drawing functions
######################################################################

def makeCairoContext():
  global width, height, lineWidth
  surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
  ctx = cairo.Context(surface)
  ctx.set_line_width(lineWidth)
  setColor(ctx, 'white')
  ctx.rectangle(0, 0, width, height)
  ctx.fill()
  return (ctx, surface)

# Returns barDelta, wBar.
def barMetrics(w, numBars, barMarginPerc=None):
  if barMarginPerc is None:
    barMarginPerc = 0.6 if numBars <= 6 else 0.35
    if w < 100: barMarginPerc = 0
    if numBars < 5: barMarginPerc = 0.2
  #print('barMetrics(%f, %d, %f)' % (w, numBars, barMarginPerc))
  barDelta = w / (numBars - barMarginPerc)
  wBar = max((1 - barMarginPerc) * barDelta, 1)
  #print('In barMetrics; wBar=%f, barDelta=%f' % (wBar, barDelta))
  return (barDelta, wBar)

def drawBarGraph(barHeights, barMax, ctx, box, barColors=None,
                 barMarginPerc=None, forcedBarWidth=None):
  top = box['top']
  left = box['left']
  w = box['width']
  h = box['height']

  isSmall = (w < 100)

  numBars = sum([0.5 if height is None else 1.0 for height in barHeights]) 
  barDelta, wBar = barMetrics(w, numBars, barMarginPerc)
  if forcedBarWidth:
    excess = forcedBarWidth - wBar
    wBar = forcedBarWidth
    barDelta -= excess / (numBars - 1)

  setColor(ctx, 'label' if isSmall else 'mainBar')
  xBar = left
  for idx, barHeight in enumerate(barHeights):
    if barHeight is None:
      xBar += (barDelta / 2)
      continue
    hBar = int(h * barHeight / barMax)
    yBar = top + h - hBar
    if barColors: ctx.set_source_rgb(*barColors[idx])
    ctx.rectangle(xBar, yBar, wBar, hBar)
    ctx.fill()
    xBar += barDelta

# Returns barHeights, perms
def getRuntimesForSorting(n, sortTimes=False):
  # Compute the bar heights.
  barHeights = [[], []]   # barHeights[<sort_idx>][<perm_idx>]
  perms = []              # perms[<perm_idx>]
  for i, fn in enumerate([quicksorted, mergesorted]):
    for perm in permsOfLen(n):
      if i == 0: perms.append(perm[:])  # Keep a copy since original may change.
      barHeights[i].append(calcNumCompares(perm, fn))
    if sortTimes:
      barHeights[i].sort()
      if i: barHeights[i].reverse()
    print('max comparisons for %s is %d' % (fn.func_name, max(barHeights[i])))
  return barHeights, perms

def drawTimeGraph(n, ctx, box, drawPerms=True, sortTimes=False):
  print('n=%d' % n)
  barHeights, perms = getRuntimesForSorting(n, sortTimes)
  if False:
    # Compute the bar heights.
    barHeights = [[], []]   # barHeights[<sort_idx>][<perm_idx>]
    perms = []              # perms[<perm_idx>]
    for i, fn in enumerate([quicksorted, mergesorted]):
      for perm in permsOfLen(n):
        if i == 0: perms.append(perm)
        barHeights[i].append(calcNumCompares(perm, fn))
      if sortTimes:
        barHeights[i].sort()
        if i: barHeights[i].reverse()
    numBars = len(perms)

  # Compute geometry guides.

  ## We have two equally-sized boxes with a margin between them.
  barMax = max(max(barHeights[0]), max(barHeights[1]))
  top = box['top']
  left = box['left']
  w = box['width']
  h = box['height']

  margin = 100
  wGraph = int((w - margin) / 2)
  hGraph = h
  xGraph = [left, left + wGraph + margin]

  if False:
    ctx.set_source_rgb(0, 0, 0)
    ctx.rectangle(left, top, w, h)
    ctx.stroke()

  barAreaHeight = int(h * 0.8)
  permTopMargin = 5
  permTop = top + barAreaHeight + permTopMargin
  permHeight = h - (barAreaHeight + permTopMargin)

  barDelta, wBar = barMetrics(wGraph, len(perms))

  # Draw the time complexity graph

  for sortIdx in range(2):
    graphBox = {'left': xGraph[sortIdx], 'top': top, 'width': wGraph, 'height': barAreaHeight}
    drawBarGraph(barHeights[sortIdx], barMax, ctx, graphBox)

  # Draw the permutations

  if drawPerms:
    x = left
    permBox = {'top': permTop, 'width': wBar, 'height': permHeight}
    for perm in perms:
      permBox['left'] = x
      drawBarGraph(perm, n, ctx, permBox)
      permBox['left'] = x + wGraph + margin
      drawBarGraph(perm, n, ctx, permBox)
      x += barDelta

  # Draw the central axis

  xMid = left + wGraph + margin / 2
  yMaxTop = top + h
  yBottom = top + barAreaHeight
  xTick = []
  for sortIdx in range(2):
    dir = 1 - 2 * sortIdx  # dir is 1 for the left, and -1 for the right graph.
    graphMid = xGraph[sortIdx] + wGraph / 2
    xTick.append(graphMid + (wGraph * 0.5 + margin * 0.42) * dir)
  for sortIdx in range(2):
    yMax = int(top + barAreaHeight * (1 - max(barHeights[sortIdx]) / float(barMax))) + 0.5
    if yMax < yMaxTop: yMaxTop = yMax
    setColor(ctx, 'label')
    ctx.move_to(xTick[sortIdx], yMax)
    ctx.line_to(xMid, yMax)
    ctx.stroke()
  ctx.move_to(xMid, yMaxTop)
  ctx.line_to(xMid, yBottom)
  ctx.stroke()
  ctx.move_to(xTick[0], yBottom)
  ctx.line_to(xTick[1], yBottom)
  ctx.stroke()


# Expects top, height to be sent in (use names for readability in the call),
# and exactly one of width or horizInset to be set.
def centeredRect(top=None, height=None, width=None, horizInset=None):
  w = globals()['width']
  if width is None: width = w - 2 * horizInset
  left = horizInset if horizInset else int((w - width) / 2)
  return {'left': left, 'top': top, 'width': width, 'height': height}

def setColor(ctx, colorName):
  colors = {
      'white': (1, 1, 1),
      'black': (0, 0, 0),
      'mainBar': (0.3, 0.43, 0.67),
      'label': (0.78, 0.82, 0.85)
  }
  ctx.set_source_rgb(*colors[colorName])


