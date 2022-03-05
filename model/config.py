class Config(object):
    def __init__(self, drive, spread, youtube, query):
        self._drive = drive
        self._spread = spread
        self._youtube = youtube
        self._query = query

    @property
    def drive(self):
        return self._drive

    @property
    def spread(self):
        return self._spread

    @property
    def youtube(self):
        return self._youtube

    @property
    def query(self):
        return self._query
