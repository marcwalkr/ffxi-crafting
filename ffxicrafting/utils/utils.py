def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def unique_preserve_order(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]
