from functools import lru_cache
from database import Database
from models import Npc


class NpcController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    @lru_cache(maxsize=None)
    def get_npc_by_name(cls, name):
        npc_tuple = cls.db.get_npc_by_name(name)

        if npc_tuple is not None:
            return Npc(*npc_tuple)
        else:
            return None
