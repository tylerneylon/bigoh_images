# bigoh.py
#
# Sort-measuring and bar-graph-drawing functions.
#

import cairo
import random

######################################################################
# Globals
######################################################################

num_compares = 0
width = 700
height = 700
line_width = 1.0


######################################################################
# Sorting functions
######################################################################

def quicksorted(arr):
  global num_compares
  n = len(arr)
  if n < 2: return arr

  # Find left & right lists so left < pivot <= right.
  pivot, left, right = arr[0], [], []
  for item in arr[1:n]:
    num_compares += 1
    if item < pivot: left.append(item)
    else: right.append(item)
  return quicksorted(left) + [pivot] + quicksorted(right)

def mergesorted(arr):
  global num_compares
  n = len(arr)
  if n < 2: return arr

  # 1. Split in half.
  mid = int(n / 2)
  left = mergesorted(arr[0:mid])
  right = mergesorted(arr[mid:n])

  # 2. Merge together.
  sorted, i, j = [], 0, 0
  while len(sorted) < n:
    num_compares += 1
    if left[i] < right[j]:
      sorted.append(left[i])
      i += 1
    else:
      sorted.append(right[j])
      j += 1
    if i == len(left): sorted += right[j:]
    if j == len(right): sorted += left[i:]
  return sorted

def randomized_quicksorted(arr):
  global num_compares
  n = len(arr)
  if n < 2: return arr

  # Set up arr[0] as a random pivot.
  pivot_index = random.randint(0, n - 1)
  arr[0], arr[pivot_index] = arr[pivot_index], arr[0]  # Item swap.

  # Find left & right lists so left < pivot <= right.
  pivot, left, right = arr[0], [], []
  for item in arr[1:n]:
    num_compares += 1
    if item < pivot: left.append(item)
    else: right.append(item)
  return quicksorted(left) + [pivot] + quicksorted(right)

def calc_num_compares(arr, fn):
  global num_compares
  num_compares = 0
  fn(arr)
  return num_compares

# Returns m', value.
def get_val_with_mod(m, mx):
  return (int(m / mx), m % mx)

# This is Algorithm L in section 7.2.1.2 of Knuth's
# Art of Computer Programming, Volume 4A.
def perms_of_len(n):
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

def perms_of_len_alternative(n):
  i = 0
  while True:
    m = i
    arr = range(1, n + 1)
    for j in range(n):
      m, val = get_val_with_mod(m, n - j)
      arr[j], arr[val + j] = arr[val + j], arr[j]
    if i > 0 and arr == range(1, n + 1): return
    yield arr
    i += 1


######################################################################
# Drawing functions
######################################################################

def make_cairo_context():
  global width, height, line_width
  surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
  ctx = cairo.Context(surface)
  ctx.set_line_width(line_width)
  set_color(ctx, 'white')
  ctx.rectangle(0, 0, width, height)
  ctx.fill()
  return (ctx, surface)

# Returns bar_delta, w_bar.
def bar_metrics(w, num_bars, bar_margin_perc=None):
  if bar_margin_perc is None:
    bar_margin_perc = 0.6 if num_bars <= 6 else 0.35
    if w < 100: bar_margin_perc = 0
    if num_bars < 5: bar_margin_perc = 0.2
  #print('bar_metrics(%f, %d, %f)' % (w, num_bars, bar_margin_perc))
  bar_delta = w / (num_bars - bar_margin_perc)
  w_bar = max((1 - bar_margin_perc) * bar_delta, 1)
  #print('In bar_metrics; w_bar=%f, bar_delta=%f' % (w_bar, bar_delta))
  return (bar_delta, w_bar)

def draw_bar_graph(bar_heights, bar_max, ctx, box, bar_colors=None,
                 bar_margin_perc=None, forced_bar_width=None):
  top = box['top']
  left = box['left']
  w = box['width']
  h = box['height']

  is_small = (w < 100)

  num_bars = sum([0.5 if height is None else 1.0 for height in bar_heights]) 
  bar_delta, w_bar = bar_metrics(w, num_bars, bar_margin_perc)
  if forced_bar_width:
    excess = forced_bar_width - w_bar
    w_bar = forced_bar_width
    bar_delta -= excess / (num_bars - 1)

  set_color(ctx, 'label' if is_small else 'main_bar')
  x_bar = left
  for idx, bar_height in enumerate(bar_heights):
    if bar_height is None:
      x_bar += (bar_delta / 2)
      continue
    h_bar = int(h * bar_height / bar_max)
    y_bar = top + h - h_bar
    if bar_colors: ctx.set_source_rgb(*bar_colors[idx])
    ctx.rectangle(x_bar, y_bar, w_bar, h_bar)
    ctx.fill()
    x_bar += bar_delta

# Returns bar_heights, perms
def get_runtimes_for_sorting(n, sort_times=False):
  # Compute the bar heights.
  bar_heights = [[], []]   # bar_heights[<sort_idx>][<perm_idx>]
  perms = []              # perms[<perm_idx>]
  for i, fn in enumerate([quicksorted, mergesorted]):
    for perm in perms_of_len(n):
      if i == 0: perms.append(perm[:])  # Keep a copy since original may change.
      bar_heights[i].append(calc_num_compares(perm, fn))
    if sort_times:
      bar_heights[i].sort()
      if i: bar_heights[i].reverse()
    print('max comparisons for %s is %d' % (fn.func_name, max(bar_heights[i])))
  return bar_heights, perms

def draw_time_graph(n, ctx, box, draw_perms=True, sort_times=False):
  print('n=%d' % n)
  bar_heights, perms = get_runtimes_for_sorting(n, sort_times)
  if False:
    # Compute the bar heights.
    bar_heights = [[], []]   # bar_heights[<sort_idx>][<perm_idx>]
    perms = []              # perms[<perm_idx>]
    for i, fn in enumerate([quicksorted, mergesorted]):
      for perm in perms_of_len(n):
        if i == 0: perms.append(perm)
        bar_heights[i].append(calc_num_compares(perm, fn))
      if sort_times:
        bar_heights[i].sort()
        if i: bar_heights[i].reverse()
    num_bars = len(perms)

  # Compute geometry guides.

  ## We have two equally-sized boxes with a margin between them.
  bar_max = max(max(bar_heights[0]), max(bar_heights[1]))
  top = box['top']
  left = box['left']
  w = box['width']
  h = box['height']

  margin = 100
  w_graph = int((w - margin) / 2)
  h_graph = h
  x_graph = [left, left + w_graph + margin]

  if False:
    ctx.set_source_rgb(0, 0, 0)
    ctx.rectangle(left, top, w, h)
    ctx.stroke()

  bar_area_height = int(h * 0.8)
  perm_topMargin = 5
  perm_top = top + bar_area_height + perm_topMargin
  perm_height = h - (bar_area_height + perm_topMargin)

  bar_delta, w_bar = bar_metrics(w_graph, len(perms))

  # Draw the time complexity graph

  for sort_idx in range(2):
    graph_box = {'left': x_graph[sort_idx], 'top': top, 'width': w_graph, 'height': bar_area_height}
    draw_bar_graph(bar_heights[sort_idx], bar_max, ctx, graph_box)

  # Draw the permutations

  if draw_perms:
    x = left
    perm_box = {'top': perm_top, 'width': w_bar, 'height': perm_height}
    for perm in perms:
      perm_box['left'] = x
      draw_bar_graph(perm, n, ctx, perm_box)
      perm_box['left'] = x + w_graph + margin
      draw_bar_graph(perm, n, ctx, perm_box)
      x += bar_delta

  # Draw the central axis

  x_mid = left + w_graph + margin / 2
  y_max_top = top + h
  y_bottom = top + bar_area_height
  x_tick = []
  for sort_idx in range(2):
    dir = 1 - 2 * sort_idx  # dir is 1 for the left, and -1 for the right graph.
    graph_mid = x_graph[sort_idx] + w_graph / 2
    x_tick.append(graph_mid + (w_graph * 0.5 + margin * 0.42) * dir)
  for sort_idx in range(2):
    y_max = int(top + bar_area_height * (1 - max(bar_heights[sort_idx]) / float(bar_max))) + 0.5
    if y_max < y_max_top: y_max_top = y_max
    set_color(ctx, 'label')
    ctx.move_to(x_tick[sort_idx], y_max)
    ctx.line_to(x_mid, y_max)
    ctx.stroke()
  ctx.move_to(x_mid, y_max_top)
  ctx.line_to(x_mid, y_bottom)
  ctx.stroke()
  ctx.move_to(x_tick[0], y_bottom)
  ctx.line_to(x_tick[1], y_bottom)
  ctx.stroke()


# Expects top, height to be sent in (use names for readability in the call),
# and exactly one of width or horiz_inset to be set.
def centered_rect(top=None, height=None, width=None, horiz_inset=None):
  w = globals()['width']
  if width is None: width = w - 2 * horiz_inset
  left = horiz_inset if horiz_inset else int((w - width) / 2)
  return {'left': left, 'top': top, 'width': width, 'height': height}

def set_color(ctx, color_name):
  colors = {
      'white': (1, 1, 1),
      'black': (0, 0, 0),
      'main_bar': (0.3, 0.43, 0.67),
      'label': (0.78, 0.82, 0.85)
  }
  ctx.set_source_rgb(*colors[color_name])


