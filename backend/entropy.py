# Author: Faisal Almuhaysh
# Implementation: Written by author

import math


def entropy(probs):
    h = 0.0
    for p in probs:
        if p > 0:
            h -= p * math.log2(p)
    return round(h, 4)


def max_entropy(n):
    if n <= 1:
        return 0.0
    return round(math.log2(n), 4)
