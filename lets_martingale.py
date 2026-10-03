"""Spread capital over a price ladder, bidding heavier towards the range end.

Each tick n (0 at range start, N-1 at range end) gets a weight w(n). A fixed
`base` share of the capital is split evenly across every tick, and the rest is
split in proportion to the weights:

    bid(n) = base * capital / N  +  (1 - base) * capital * w(n) / sum(w)

so the bids always add up to exactly `capital`, whatever N or w.
"""

import argparse
from math import floor

EPSILON = 1e-9


# Weight functions: tick n -> relative weight. Only the shape matters; the
# allocation normalises them.
def linear(n, ticks):
  return n + 1


def power(exponent):
  return lambda n, ticks: (n + 1) ** exponent


def martingale(ratio):
  # ratio ** n, written relative to the last tick so it never overflows
  return lambda n, ticks: ratio ** (n - (ticks - 1))


WEIGHTS = {
  "linear": lambda arg: linear,
  "power": lambda arg: power(2.0 if arg is None else arg),
  "martingale": lambda arg: martingale(2.0 if arg is None else arg),
}


def price_ladder(start, end, step):
  if step <= 0:
    raise ValueError("step must be positive")
  span = abs(end - start)
  direction = -1 if end < start else 1
  # The epsilon stops float error (0.2 / 0.1 = 1.9999...) dropping the last tick
  ticks = floor(span / step + EPSILON) + 1
  return [round(start + direction * n * step, 10) for n in range(ticks)]


def allocate(capital, ticks, weight, base):
  if capital <= 0:
    raise ValueError("capital must be positive")
  if not 0 <= base <= 1:
    raise ValueError("base must be between 0 and 1")
  weights = [weight(n, ticks) for n in range(ticks)]
  if any(w < 0 for w in weights) or sum(weights) <= 0:
    raise ValueError("weights must be non-negative with a positive sum")
  floor_bid = base * capital / ticks
  weighted = (1 - base) * capital
  return [floor_bid + weighted * w / sum(weights) for w in weights]


def lets_martingale(capital, start, end, step, weight, base):
  prices = price_ladder(start, end, step)
  bids = allocate(capital, len(prices), weight, base)
  return list(zip(prices, bids))


def report(capital, start, end, rows):
  coins = sum(bid / price for price, bid in rows)
  lines = [
    "==============",
    "Deploy ${:,.2f} over the range [{:g}, {:g}]".format(capital, start, end),
    "==============",
    *("${:<10g} {:>10.2f} {:>8.4f}Ξ".format(p, b, b / p) for p, b in rows),
    "==============",
    "Capital used: {:.2f}".format(sum(bid for _, bid in rows)),
    "Average entry if fully filled: ${:.2f} ({:.4f}Ξ)".format(capital / coins, coins),
  ]
  return "\n".join(lines)


def main():
  parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
  parser.add_argument("--capital", type=float, default=10000)
  parser.add_argument("--start", type=float, default=2000, help="first bid price")
  parser.add_argument("--end", type=float, default=1000, help="range-end bid price")
  parser.add_argument("--step", type=float, default=100)
  parser.add_argument("--weight", choices=WEIGHTS, default="power")
  parser.add_argument(
    "--arg", type=float, help="power exponent (default 2) or martingale ratio (default 2)"
  )
  parser.add_argument(
    "--base", type=float, default=0.3, help="share of capital spread evenly (0-1)"
  )
  args = parser.parse_args()
  weight = WEIGHTS[args.weight](args.arg)
  rows = lets_martingale(args.capital, args.start, args.end, args.step, weight, args.base)
  print(report(args.capital, args.start, args.end, rows))


if __name__ == "__main__":
  main()
