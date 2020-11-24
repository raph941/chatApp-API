from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.security.websocket import OriginValidator


from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': OriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                url(r"^chat/$", ChatConsumer),
            ])
        ),
        ['*'],
    ) 
})