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
            items_end = stripped[items_start:].index(
                "}") + before_stock_length
            item_lines = stripped[items_start+1:items_end]

            for line in item_lines:
                # If the line has too many dashes, the item was commented out,
                # skip those lines and any empty lines
                dash_count = len(re.findall("-", line))
                if dash_count > 2 or len(line) < 1:
                    continue

                # The item_id and price are the first 2 numbers on the line
                numbers = re.findall('[0-9]+', line)

                try:
                    item_id, price = numbers[0:2]
                except ValueError:
                    continue

                comment_start = line.index("--")
                item_comment = line[comment_start:]
                if item_comment[2] != " ":
                    item_comment = "-- " + item_comment[2:]

                insert_statement = ("INSERT INTO vendor_items VALUES "
                                    "({},{},{});\t{}".format(item_id,
                                                             npc_id,
                                                             price,
                                                             item_comment))
                file_lines.append(insert_statement)

            file_lines.append("")

    with open("vendor_inserts.txt", "w") as writer:
        for line in file_lines:
            writer.write(line + "\n")
