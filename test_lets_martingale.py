import unittest

from lets_martingale import allocate, lets_martingale, linear, martingale, power, price_ladder


class PriceLadderTest(unittest.TestCase):
  def test_descending_range_includes_range_end(self):
    self.assertEqual(price_ladder(2000, 1000, 250), [2000, 1750, 1500, 1250, 1000])

  def test_float_step_keeps_last_tick(self):
    self.assertEqual(price_ladder(0.3, 0.1, 0.1), [0.3, 0.2, 0.1])

  def test_ascending_range(self):
    self.assertEqual(price_ladder(1, 3, 1), [1, 2, 3])

  def test_rejects_non_positive_step(self):
    with self.assertRaises(ValueError):
      price_ladder(2000, 1000, 0)


class AllocateTest(unittest.TestCase):
  def test_sums_to_capital_for_any_tick_count(self):
    # The original crashed once ticks * initial_percentage passed 100%
    for step in (100, 50, 10, 1):
      rows = lets_martingale(10000, 2000, 1000, step, power(2), 0.3)
      self.assertAlmostEqual(sum(bid for _, bid in rows), 10000, places=6)

  def test_bids_increase_towards_range_end(self):
    for weight in (linear, power(2), martingale(2)):
      bids = allocate(10000, 11, weight, 0.3)
      self.assertEqual(bids, sorted(bids))

  def test_martingale_doubles_weighted_part(self):
    bids = allocate(700, 3, martingale(2), 0)
    self.assertEqual([round(b, 9) for b in bids], [100, 200, 400])

  def test_martingale_does_not_overflow_with_many_ticks(self):
    bids = allocate(10000, 5000, martingale(2), 0.3)
    self.assertAlmostEqual(sum(bids), 10000, places=6)

  def test_full_base_is_flat(self):
    self.assertEqual(allocate(900, 3, power(2), 1), [300, 300, 300])

  def test_rejects_base_outside_unit_interval(self):
    with self.assertRaises(ValueError):
      allocate(10000, 11, linear, 1.5)


if __name__ == "__main__":
  unittest.main()
