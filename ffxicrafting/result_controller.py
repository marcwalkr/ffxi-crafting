from database import Database
from synthesis_result import SynthesisResult


class ResultController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_results(cls, item_name):
        result_tuples = cls.db.get_synthesis_results(item_name)

        results = []
        for result_tuple in result_tuples:
            result = SynthesisResult(*result_tuple)
            results.append(result)

        return results

    @classmethod
    def get_all_results(cls):
        result_tuples = cls.db.get_all_synthesis_results()

        results = []
        for result_tuple in result_tuples:
            result = SynthesisResult(*result_tuple)
            results.append(result)

        return results

    @classmethod
    def add_result(cls, item_name, recipe_id, quantity, quality_level):
        result = SynthesisResult(item_name, recipe_id, quantity, quality_level)
        cls.db.add_synthesis_result(result)
