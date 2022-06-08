class GuildShop:
    def __init__(self, guild_id, item_id, min_price, max_price, max_quantity,
                 daily_increase, initial_quantity) -> None:
        self.guild_id = guild_id
        self.item_id = item_id
        self.min_price = min_price
        self.max_price = max_price
        self.max_quantity = max_quantity
        self.daily_increase = daily_increase
        self.initial_quantity = initial_quantity
