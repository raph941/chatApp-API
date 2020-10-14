import asyncio
import json
import datetime
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.core.exceptions import ValidationError
from django.core import serializers
from channels.generic.websocket import WebsocketConsumer

from chat.apps import MessagingService as Ms
from chat.models import Message, ChatRoom
from serializers.chat_serializers import ConvMessageSerializer
from accounts.models import User
from .socket_request_types import *
from channels.consumer import SyncConsumer
from django.http import JsonResponse


class ChatConsumer(SyncConsumer):

    def websocket_connect(self, event):
        """event triggered when connection handshake is succesful"""
        self.send({'type': 'websocket.accept'})

    def websocket_receive(self, event):
        """event triggered when a message is sent to the socket"""

        text_data = event.get('text', None)
        data_json = json.loads(text_data)
        _type = data_json.get('type')
        data = data_json.get('payload')
        room = self.get_conv_room(data.get('uid1'), data.get('uid2'))
        self.chat_room_name = f'chat_{room.id}'

        if _type == START_CHAT: 
            self.handleGroupAdd(data.get('uid1'), data.get('uid2'))
        elif _type == SEND_NEW_MESSAGE: 
            message, created = self.send_msg(data.get('uid1'), data.get('uid2'), data.get('message'))
            serialized_data = self.serialize(message)

            # Send message to room group
            print('here')
            async_to_sync(self.channel_layer.group_send)(
                self.chat_room_name,
                {
                    'type': 'chat_message',
                    'message': serialized_data
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        # import pdb ; pdb.set_trace()
        message = json.dumps(event.get('message'))

        self.send({
            "type": "websocket.send",
            "text": message
        })

    
    def send(self, message):
        """
        Overrideable/callable-by-subclasses send method.
        """
        self.base_send(message)

    def websocket_disconnect(self, close_code):
        pass


    def handleGroupAdd(self, pk1, pk2):
        """
        creates channel group for the two users to chat in.
        pk1, pk2 : integers representing the two user's pk
        roomid int: chat room
        """

        # import pdb ; pdb.set_trace()
        async_to_sync(self.channel_layer.group_add)(
            self.chat_room_name,
            self.channel_name
        )
        print('layer added')


    def serialize(self, message):
        return ConvMessageSerializer(message).data

    def get_conv_room(self, pk1, pk2):
        return Ms.get_conversation_room(pk1, pk2)


    def send_msg(self, sender, recipient, message):
        return Ms.send_message(sender, recipient, message)