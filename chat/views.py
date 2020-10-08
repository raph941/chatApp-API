from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, GenericAPIView
from serializers.chat_serializers import ConvPartnerSerializer, ConvMessageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from chat.apps import MessagingService

class ConvPartnerView(ListAPIView):
    """ Returns a list people a user has made a conversation with """
    serializer_class = ConvPartnerSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query = MessagingService.get_conversations(self.request.user)
        return query


class ConvMessageView(ListAPIView):
    """ Returns a list of messages Between two users """
    serializer_class = ConvMessageSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        other_guy_id    = self.kwargs.get('pk') 
        me              = self.request.user
        query = MessagingService.get_conversation(me, other_guy_id, limit=50, mark_read=True)
        return query