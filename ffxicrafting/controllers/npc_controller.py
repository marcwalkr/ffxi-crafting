from models import Npc


class NpcController:
    cache = {}

    def __init__(self, db) -> None:
        self.db = db

    def get_npc(self, npc_id):
        if npc_id in self.cache:
            return self.cache[npc_id]
        else:
            npc_tuple = self.db.get_npc(npc_id)
            if npc_tuple is not None:
                self.cache[npc_id] = Npc(*npc_tuple)
                return self.cache[npc_id]
            else:
                return None
