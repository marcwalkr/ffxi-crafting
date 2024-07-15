def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def unique_preserve_order(original_list):
    seen = set()
    unique_list = []

    for item in original_list:
        if item not in seen:
            seen.add(item)
            unique_list.append(item)

    return unique_list
