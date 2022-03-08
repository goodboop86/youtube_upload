class YoutubeRequestParam(object):
    def __init__(self, params):
        """
        :param params:
        {"date":"YYYY-MM-DD", "file":"***", "title":"***","description":"this is ..." , "categoryId":int,
        "tags": "tag1, tag2, ...", "privacyStatus":"public"}
        """

        self._date = params["date"]
        self._file = params["file"]
        self._title = params["title"]
        self._description = params["description"]
        self._category_id = params["categoryId"]
        self._tags = params["tags"]
        self._privacy_status = params["privacyStatus"]
        self._mov_mp4 = f"{params['date']}/{params['file']}.mp4"
        self._img_png = f"{params['date']}/{params['file']}.png"

        del params['file'], params['date'], params['privacyStatus']
        self._request = {"snippet": params, "status": {"privacyStatus": self._privacy_status}}
        self._mov_id = None

    @property
    def date(self):
        return self._date

    @property
    def file(self):
        return self._file

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def category_id(self):
        return self._category_id

    @property
    def tags(self):
        return self._tags

    @property
    def privacy_status(self):
        return self._privacy_status

    @property
    def mov_mp4(self):
        return self._mov_mp4

    @property
    def img_png(self):
        return self._img_png

    @property
    def request(self):
        return self._request

    @property
    def mov_id(self):
        return self._mov_id

    @mov_id.setter
    def mov_id(self, value):
        self._mov_id = value
