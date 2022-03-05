class ApiClient(object):
    def __init__(self, drive, spread, youtube):
        self._drive = drive
        self._spread = spread
        self._youtube = youtube

    @property
    def drive(self):
        return self._drive

    @property
    def spread(self):
        return self._spread

    @property
    def youtube(self):
        return self._youtube
