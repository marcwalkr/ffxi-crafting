from models import Npc


class NpcController:
    _cache = {}

    def __init__(self, db) -> None:
        self.db = db

    def get_npc(self, npc_id):
        if npc_id in self._cache:
            return self._cache[npc_id]
        else:
            npc_tuple = self.db.get_npc(npc_id)
            if npc_tuple is not None:
                self._cache[npc_id] = Npc(*npc_tuple)
                return self._cache[npc_id]
            else:
                return None
