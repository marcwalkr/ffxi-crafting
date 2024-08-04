def clamp(n: float, minn: float, maxn: float) -> float:
    """
    Constrain a number within a specified range.

    Ensures that the given number "n" falls within the range defined by
    "minn" and "maxn". If "n" is less than "minn", it returns "minn".
    If "n" is greater than "maxn", it returns "maxn". Otherwise, it returns "n".

    Args:
        n (float): The number to be clamped.
        minn (float): The minimum allowed value.
        maxn (float): The maximum allowed value.

    Returns:
        float: The clamped value of "n", which will be between "minn" and "maxn", inclusive.
    """
    return max(min(maxn, n), minn)
