from database import Database
from models import RecipeModel


class RecipeRepository:
    """
    Repository class for handling recipe-related data operations.

    This class provides methods to interact with the database for retrieving
    recipe information.
    """

    _cache: list[RecipeModel] = []

    def __init__(self, db: Database) -> None:
        """
        Initialize a RecipeRepository instance.
        All recipes are loaded into the cache on initialization.

        Args:
            db (Database): The database connection object used for querying recipe data.
        """
        self._db = db
        if not RecipeRepository._cache:
            self._load_recipes()

    def _load_recipes(self) -> None:
        """
        Load all recipes into the cache.
        """
        recipe_tuples = self._db.get_all_recipes()
        recipe_models = [RecipeModel(*tuple) for tuple in recipe_tuples]
        RecipeRepository._cache = recipe_models

    def get_all_recipes(self) -> list[RecipeModel]:
        """
        Retrieve all recipe models.

        Returns:
            list[RecipeModel]: A list of RecipeModel objects.
        """
        return self._cache

    def delete_cache(self) -> None:
        """
        Delete the cache.
        """
        self._cache = []
