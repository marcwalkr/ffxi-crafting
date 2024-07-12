import os
import re
from controllers.npc_controller import NpcController


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


def generate_vendor_inserts():
    file_lines = []

    for filename in os.listdir("vendor_files"):
        file = os.path.join("vendor_files", filename)

        with open(file) as f:
            npc_name = filename.split(".")[0]
            npc_name = npc_name.replace("_", " ")
            npc = NpcController.get_npc_by_name(npc_name)
            npc_id = npc.npc_id

            npc_name_comment = "-- {}".format(npc_name)
            file_lines.append(npc_name_comment)

            lines = f.readlines()
            stripped_lines = [s.strip() for s in lines]

            for line in stripped_lines:
                # The line has 2 numbers separated by a comma and a comment
                # e.g. 13327, 1250, -- Silver Earring
                if not re.search(r"\d+,\s*\d+.*--.+", line):
                    continue

                # The item_id and price are the first 2 numbers on the line
                numbers = re.findall("[0-9]+", line)
                item_id, price = numbers[0:2]

                comment_start = line.index("--")
                item_comment = line[comment_start:]
                # Add a space after the -- if there isn't already
                if item_comment[2] != " ":
                    item_comment = "-- " + item_comment[2:]

                insert_statement = ("INSERT INTO vendor_items VALUES "
                                    "({},{},{});\t{}".format(item_id,
                                                             npc_id,
                                                             price,
                                                             item_comment))

                if insert_statement not in file_lines:
                    file_lines.append(insert_statement)

            file_lines.append("")

    with open("vendor_inserts.txt", "w") as writer:
        for line in file_lines:
            writer.write(line + "\n")
