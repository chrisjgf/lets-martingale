# lets-martingale
Little script to weight bids heavier when the price is closer to range-end.  [Martingale](https://en.wikipedia.org/wiki/Martingale_%28probability_theory%29) inspired

Each tick `n` on the ladder (0 at the start price, `N-1` at range-end) is put through a weight
function `w(n)`. A `base` share of the capital is spread evenly over every tick and the rest is split
in proportion to the weights:

    bid(n) = base * capital / N  +  (1 - base) * capital * w(n) / sum(w)

The bids always add up to exactly `capital`, however many ticks there are.

| `--weight` | `w(n)` | `--arg` |
| --- | --- | --- |
| `linear` | `n + 1` | unused |
| `power` (default) | `(n + 1) ** p` | exponent `p`, default 2 |
| `martingale` | `r ** n` | ratio `r`, default 2 (classic doubling) |

To add another shape, write a function `(n, ticks) -> weight` and register it in `WEIGHTS`.

    python3 lets_martingale.py --capital 10000 --start 2000 --end 1000 --step 100 --weight power --base 0.3

    ==============
    Deploy $10,000.00 over the range [2000, 1000]
    ==============
    $2000           286.56   0.1433Ξ
    $1900           328.06   0.1727Ξ
    $1800           397.23   0.2207Ξ
    $1700           494.07   0.2906Ξ
    $1600           618.58   0.3866Ξ
    $1500           770.75   0.5138Ξ
    $1400           950.59   0.6790Ξ
    $1300          1158.10   0.8908Ξ
    $1200          1393.28   1.1611Ξ
    $1100          1656.13   1.5056Ξ
    $1000          1946.64   1.9466Ξ
    ==============
    Capital used: 10000.00
    Average entry if fully filled: $1264.09 (7.9108Ξ)

Tests: `python3 -m unittest`
