from core.common.pattern.singleton import singleton
from .exceptions import YamlLoadException
import yaml


@singleton
class ConfigLoader:
    config = None

    def load(self, path):
        try:
            with open(path, 'r') as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
            return self.config
        except YamlLoadException as e:
            print(e)
            return None
