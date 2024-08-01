from models import RecipeModel


class RecipeRepository:
    all_result_item_ids = None

    def __init__(self, db):
        self.db = db

    def get_all_result_item_ids(self):
        if self.all_result_item_ids is None:
            self.all_result_item_ids = self.db.get_all_result_item_ids()
        return self.all_result_item_ids

    def is_craftable(self, item_id):
        return item_id in self.get_all_result_item_ids()
