class Config(object):
    def __init__(self, conf):
        self._config = conf

    def get(self, property_name):
        if property_name not in self._config.keys():
            return None
        return self._config[property_name]
