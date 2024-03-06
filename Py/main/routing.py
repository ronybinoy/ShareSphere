from django.urls import path
from . import consumers1

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    path('messages_page/', consumers1.ChatConsumer1.as_asgi()),
]



