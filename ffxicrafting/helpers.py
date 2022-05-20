import collections


def add_nones(a_list, num):
    """Appends a number of empty strings to the end of a list"""
    with_nones = a_list + [None] * num
    return with_nones


def remove_nones(a_list):
    """Removes all empty strings from a list"""
    return list(filter(None, a_list))


def sort_alphabetically(obj_list):
    """Sorts a list of objects with a name attribute alphabetically"""
    sorted_list = sorted(obj_list, key=lambda x: x.name)
    return sorted_list


def same_elements(list1, list2):
    return collections.Counter(list1) == collections.Counter(list2)
