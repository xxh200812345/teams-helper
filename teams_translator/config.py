import yaml
import threading

class Settings:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Settings, cls).__new__(cls)
                    cls._instance._load()
        return cls._instance

    def _load(self):
        with open("settings.yaml", "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

    def get(self) -> dict:
        val = self.data
        return val