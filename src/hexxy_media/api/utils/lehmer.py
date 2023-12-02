from typing import Sequence


def swizzle(*, start: Sequence[str], finish: Sequence[str]):
    """
    Given a target stack state, compute the Lehmer code (Swindler's input) which
    transforms the given start state to the target state. Stack states are written
    bottom to top, left to right. If the start state is not given, defaults to a stack
    of characters (up to 26) with 'a' at top and 'z' at bottom.
    """

    n = len(finish)
    if n > len(start):
        raise ValueError("too few stack elems")

    start = list(start)[-n:]

    stack = [1]
    for i in range(1, n):
        stack.append(stack[-1] * i)

    count = 0
    for val in finish:
        ix = start.index(val)
        count += stack.pop() * ix
        del start[ix]

    return count
