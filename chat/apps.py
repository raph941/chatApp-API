from django.apps import AppConfig
from .utils import MessagingService

MessagingService = MessagingService()

class ChatConfig(AppConfig):
    name = 'chat'
