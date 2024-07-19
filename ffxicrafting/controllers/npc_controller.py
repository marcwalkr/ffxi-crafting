from models import Npc


class NpcController:
    _cache = {}

    def __init__(self, db) -> None:
        self.db = db

    def get_npc_by_name(self, name):
        if name in self._cache:
            return self._cache[name]
        else:
            npc_tuple = self.db.get_npc_by_name(name)
            if npc_tuple is not None:
                self._cache[name] = Npc(*npc_tuple)
                return self._cache[name]
            else:
                return None
