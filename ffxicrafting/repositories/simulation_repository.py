import json
from models import SimulationResult
from config import SettingsManager
from functools import lru_cache


class SimulationRepository:
    def __init__(self, db) -> None:
        self.db = db
        self.beastmen_regions = json.dumps(SettingsManager.get_beastmen_regions())
        self.enabled_guilds = json.dumps(SettingsManager.get_enabled_guilds())
