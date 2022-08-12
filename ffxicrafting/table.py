from prettytable import PrettyTable


class Table:
    def __init__(self, column_labels, rows, sort_column=None,
                 reverse_sort=False) -> None:
        self.column_labels = column_labels
        self.rows = rows
        self.sort_column = sort_column
        self.reverse_sort = reverse_sort

    def print(self):
        table = PrettyTable(self.column_labels)

        for name in self.column_labels:
            table.align[name] = "l"

        for row in self.rows:
            table.add_row(row)

        if self.sort_column is not None:
            table.sortby = self.sort_column
            table.reversesort = self.reverse_sort

        print(table)
