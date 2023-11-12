from core.common.pattern.singleton import singleton
from .exceptions import YamlLoadException
from core.common.helper.nested import Nested
import yaml


@singleton
class ConfigLoader:
    config = None

    def load(self, path):
        try:
            with open(path, 'r') as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
                self.config = Nested(**self.config)
            return self.config
        except YamlLoadException as e:
            print(e)
            return None
