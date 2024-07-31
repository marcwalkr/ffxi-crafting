from models import Npc
from functools import lru_cache


class NpcRepository:
    def __init__(self, db) -> None:
        self.db = db

    @lru_cache(maxsize=None)
    def get_npc(self, npc_id):
        npc_tuple = self.db.get_npc(npc_id)
        if npc_tuple is not None:
            return Npc(*npc_tuple)
        else:
            return None
