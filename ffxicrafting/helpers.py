import os
import re
from datetime import datetime, timezone
from controllers.npc_controller import NpcController


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def get_utc_timestamp():
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)

    return utc_time.strftime("%Y-%m-%d %H:%M:%S")


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


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
                numbers = re.findall('[0-9]+', line)
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
