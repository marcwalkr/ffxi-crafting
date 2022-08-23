from database import Database
from models.bundle import Bundle


class BundleController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_bundle(cls, unbundled_id):
        bundle_tuple = cls.db.get_bundle(unbundled_id)

        if bundle_tuple is not None:
            return Bundle(*bundle_tuple)
        else:
            return None
