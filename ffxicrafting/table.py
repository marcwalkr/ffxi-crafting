from prettytable import PrettyTable


class Table:
    def __init__(self, column_labels, rows) -> None:
        self.column_labels = column_labels
        self.rows = rows

    def print(self):
        table = PrettyTable(self.column_labels)

        for name in self.column_labels:
            table.align[name] = "l"

        for row in self.rows:
            table.add_row(row)

        print(table)
