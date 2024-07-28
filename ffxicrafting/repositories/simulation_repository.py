from models import SimulationResult
from config import SettingsManager
import json


class SimulationRepository:
    cache = {}

    def __init__(self, db) -> None:
        self.db = db
        self.beastmen_regions = json.dumps(SettingsManager.get_beastmen_regions())
        self.enabled_guilds = json.dumps(SettingsManager.get_enabled_guilds())
