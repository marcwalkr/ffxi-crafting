def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def summarize_list(items):
    if not items:
        return ""

    summarized = []
    current_item = items[0]
    count = 1

    for i in range(1, len(items)):
        if items[i] == current_item:
            count += 1
        else:
            if count > 1:
                summarized.append(f"{current_item} x{count},")
            else:
                summarized.append(f"{current_item},")
            current_item = items[i]
            count = 1

    # Append the last item after loop termination
    if count > 1:
        summarized.append(f"{current_item} x{count},")
    else:
        summarized.append(f"{current_item},")

    # Join the summarized list with spaces and remove the trailing comma
    summary = " ".join(summarized).rstrip(",")

    return summary


def count_items(strings):
    count_dict = {}
    for string in strings:
        if string in count_dict:
            count_dict[string] += 1
        else:
            count_dict[string] = 1
    return count_dict


def format_item_name(item):
    return item.sort_name.replace("_", " ").title()
