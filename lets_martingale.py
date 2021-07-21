from math import sqrt, floor

# @var area                = total curve area 
# @var x                   = max of x-axis range. ie. [0...5] => 5
# @var y                   = initial c constant
def curve_gradient(area, x_max, c):
  # curve => (x/m) ** 2 + c = area
  # integral => ((x ** 3) / (3 * (m ** 2))) + c = area
  # rearranged for m
  return sqrt((x_max ** 3) / ((area - (c * x_max)) * 3))
  
# @var x                  = x-axis range / num of intervals
# @var c                  = initial constant / rough starting position
# @var m                  = gradient of curve
def curve(x, c, m):
  return ((x ** 3) / (3 * (m ** 2))) + c

# @var capital            = total capital to spend
# @var price_range        = range of bid prices
# @var step               = step to increment/decrement
# @var initial_percentage = initial starting position
def lets_martingale(capital, price_range, step, initial_percentage):
  ab_step = abs(step)
  direction = -1 if (price_range[1] - price_range[0]) < 0 else 1
  directional_step = ab_step * direction
  x_max = int(abs(price_range[1] - price_range[0]) / ab_step) + 1
  c = initial_percentage * capital
  m = curve_gradient(capital, x_max, c)
  
  print("==============")
  print("Deploy {} over the range [{}, {}]".format(capital, price_range[0], price_range[1]))
  print("==============")

  
  values = []
  for i in range(0, x_max):
    value = (curve(i+1, c, m) - curve(i, c, m)) + c
    price = price_range[0] + (i * directional_step)
    print("${}".format(price), "{0:.2f}".format(value), "{0:.2f}Ξ".format((value / price)))
    values.append(value)
  
  print("==============")
  print("Capital used:", sum(values))

lets_martingale(10000, [2000, 1000], 100, 0.03)