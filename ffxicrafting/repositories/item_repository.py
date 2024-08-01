from models import ItemModel


class ItemRepository:
    cache = {}

    def __init__(self, db) -> None:
        self.db = db

    def get_items(self, item_ids):
        # Get cached items and identify missing items
        cached_items = [self.cache[id] for id in item_ids if id in self.cache]
        missing_item_ids = [id for id in item_ids if id not in self.cache]

        # Fetch missing items from the database
        if missing_item_ids:
            item_tuples = self.db.get_items(missing_item_ids)
            new_items = [ItemModel(*tuple) for tuple in item_tuples]

            # Update cache with new items
            self.cache.update({item.item_id: item for item in new_items})

            return cached_items + new_items

        return cached_items
