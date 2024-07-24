class VendorItem:
    def __init__(self, item_id, npc_id, price, sandoria_rank, bastok_rank, windurst_rank, sandoria_citizen,
                 bastok_citizen, windurst_citizen) -> None:
        self.item_id = item_id
        self.npc_id = npc_id
        self.price = price
        self.sandoria_rank = sandoria_rank
        self.bastok_rank = bastok_rank
        self.windurst_rank = windurst_rank
        self.sandoria_citizen = sandoria_citizen
        self.bastok_citizen = bastok_citizen
        self.windurst_citizen = windurst_citizen
