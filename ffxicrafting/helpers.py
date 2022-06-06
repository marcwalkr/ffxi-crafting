import re
import os


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


def scrape_vendor_files(directory):
    vendor_data = []

    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)

        with open(file) as f:
            npc_name = filename.split(".")[0]

            lines = f.readlines()
            stripped = [s.strip() for s in lines]

            # Get the start index of the stock list by searching for one of
            # these lines
            if "local stock =" in stripped:
                items_start = stripped.index("local stock =") + 1
            elif "stock = {" in stripped:
                items_start = stripped.index("stock = {")
            else:
                items_start = stripped.index("local stock = {")

            # Get the end index of the stock list by searching for the next "}"
            before_stock_length = len(stripped[:items_start])
            items_end = stripped[items_start:].index("}") + before_stock_length
            item_lines = stripped[items_start+1:items_end]

            for line in item_lines:
                # If the line has too many dashes, the item was commented out,
                # skip those lines and any empty lines
                dash_count = len(re.findall("-", line))
                if dash_count > 2 or len(line) < 1:
                    continue

                # The item_id and price are the first 2 numbers on the line
                numbers = re.findall('[0-9]+', line)
                item_id, price = numbers[0:2]

                item_id = int(item_id)
                price = int(price)

                vendor_data.append([item_id, npc_name, price])

    return vendor_data
