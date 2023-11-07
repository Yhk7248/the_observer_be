class Nested:

    def __init__(self, **kwargs):
        if kwargs:
            for key, val in kwargs.items():
                if isinstance(val, dict):
                    setattr(self, key, Nested(**val))
                elif isinstance(val, list):
                    val = [Nested(**x) if isinstance(x, dict) else x for x in val]
                    setattr(self, key, val)
                else:
                    setattr(self, key, val)


#
#   test
#
if __name__ == "__main__":
    from core.common.loader.config_loader import ConfigLoader

    cfg = ConfigLoader().load(path='../config/config.yaml')

    a = Nested(**cfg)
