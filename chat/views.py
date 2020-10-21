from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, GenericAPIView
from serializers.chat_serializers import ConvPartnerSerializer, ConvMessageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from chat.apps import MessagingService
from accounts.models import User
import logging

logger = logging.getLogger(__name__)


class ConvPartnerView(ListAPIView):
    """ Returns a list people a user has made a conversation with """
    serializer_class = ConvPartnerSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try: return MessagingService.get_conversations(self.request.user) 
        except: pass        


class ConvMessageView(ListAPIView):
    """ Returns a list of messages Between two users """
    serializer_class = ConvMessageSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        other_guy_id    = self.kwargs.get('pk') 
        other_guy       = User.objects.get(pk=int(other_guy_id))
        me              = self.request.user
        try: return MessagingService.get_conversation(me, other_guy, limit=50)
        except: logger.info('UNABLE TO GET CONVERSATION MESSAGES BETWEEN', me, 'AND', other_guy)
        