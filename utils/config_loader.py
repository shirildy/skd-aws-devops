import os
import yaml

class ConfigLoader:
    def __init__(self, env: str, config_dir: str = 'configs'):
        self.env = env
        self.path = os.path.join(config_dir, f'config_{env}.yaml')
        self.config = self._load_yaml()

    def _load_yaml(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Config file not found: {self.path}")
        with open(self.path) as file:
            return yaml.safe_load(file)

    def get(self, section: str, key: str = None):
        if section not in self.config:
            raise KeyError(f"Missing section: {section}")
        if key:
            if key not in self.config[section]:
                raise KeyError(f"Missing key: {key} in section: {section}")
            return self.config[section][key]
        return self.config[section]

