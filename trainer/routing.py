# trainer/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/job/(?P<job_id>\w+)/$', consumers.JobConsumer.as_asgi()),
]