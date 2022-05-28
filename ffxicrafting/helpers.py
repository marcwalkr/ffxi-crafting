import re


def add_nones(a_list, num):
    """Appends a number of Nones to the end of a list"""
    with_nones = a_list + [None] * num
    return with_nones


def remove_nones(a_list):
    """Removes all empty strings from a list"""
    return list(filter(None, a_list))


def expand_list(condensed_list):
    """Removes numbers and expands list e.g. Item x3 -> Item Item Item"""
    expanded_list = []
    for ele in condensed_list:
        num_found = re.search(r"\d+", ele)
        if num_found:
            num = int(num_found.group(0))
            name_without_num = ele[:ele.rfind(" ")]
            expanded_list += [name_without_num] * num
        else:
            expanded_list.append(ele)

    return expanded_list
