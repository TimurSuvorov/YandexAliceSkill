import rapidjson

from django.http import HttpResponse


class RapidJSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        data = rapidjson.dumps(data).encode('utf-8')
        super().__init__(content=data, **kwargs)

