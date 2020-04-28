"""
Compositions of a number.
"""
import itertools
import random

def positive(n, k):
    """
    How to write n as a sum of k terms.

    See https://en.wikipedia.org/wiki/Composition_(combinatorics)

    Note there \binom{n-1}{k-1} such tuples. 

		>>> for c in positive(5, 3):
		...     print(c)
		... 
		(1, 1, 3)
		(1, 2, 2)
		(1, 3, 1)
		(2, 1, 2)
		(2, 2, 1)
		(3, 1, 1)
    """
    for comb in itertools.combinations(range(n-1), k-1):
        comb = [-1] + list(comb) + [n-1]
        diffs = [comb[i+1] - comb[i] for i in range(len(comb) - 1)]
        yield tuple(diffs)

def non_negative(n, k):
    """
    Allow for 0.

    There are \binom{n+k-1}{k-1} such compositions.
    """
    for comp in positive(n+k, k):
        yield tuple(x-1 for x in comp)


