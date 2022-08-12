class SynthRow:
    def __init__(self, recipe_id, nq_name, nq_quantity, hq1_name, hq1_quantity,
                 hq2_name, hq2_quantity, hq3_name, hq3_quantity, cost,
                 average_profit, average_frequency) -> None:
        self.recipe_id = recipe_id
        self.nq_name = nq_name
        self.nq_quantity = nq_quantity
        self.hq1_name = hq1_name
        self.hq1_quantity = hq1_quantity
        self.hq2_name = hq2_name
        self.hq2_quantity = hq2_quantity
        self.hq3_name = hq3_name
        self.hq3_quantity = hq3_quantity
        self.cost = cost
        self.average_profit = average_profit
        self.average_frequency = average_frequency

    def get(self):
        return [self.recipe_id, self.nq_name, self.nq_quantity, self.hq1_name,
                self.hq1_quantity, self.hq2_name, self.hq2_quantity,
                self.hq3_name, self.hq3_quantity, self.cost,
                self.average_profit, self.average_frequency]
