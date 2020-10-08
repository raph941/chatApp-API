from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    # 'websocket': AllowedHostsOriginValidator(
    #     AuthMiddlewareStack(
    #         URLRouter(
    #             [
    #                 url(r"^chat", ChatConsumer),
    #             ]
    #         )
    #     )
    # ) 
})