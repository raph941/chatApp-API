from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
import datetime
from django.db.models import Q

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class ChatRoomManager(models.Manager):

    def get_or_new(self, user1, user2): # get_or_create
        if user1 == user2:
            return None
        qlookup1 = Q(first=user1) & Q(second=user2)
        qlookup2 = Q(first=user2) & Q(second=user1)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user1.__class__
            user = Klass.objects.get(username=user2.username)
            if user1 != user:
                obj = self.model(
                        first=user1, 
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False

class ChatRoom(models.Model):
    """
    A thread for each message, like a room that contains two folks
    """
    first        = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
    second       = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second')
    timestamp    = models.DateTimeField(default=datetime.datetime.now())

    objects      = ChatRoomManager()

    def __int__(self):
        return self.id


class Message(models.Model):
    """
    A private directmessage
    """
    content = models.TextField(_('Content'))
    sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_dm', verbose_name=_("Sender"), on_delete=models.CASCADE)
    recipient = models.ForeignKey(AUTH_USER_MODEL, related_name='received_dm', verbose_name=_("Recipient"), on_delete=models.CASCADE)
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    room = models.ForeignKey(ChatRoom, null=True, blank=True, on_delete=models.SET_NULL)


    @property
    def unread(self):
        """returns whether the message was read or not"""
        if self.read_at is not None:
            return False
        return True

    def __str__(self):
        return self.content

    def save(self, **kwargs):
        if self.sender == self.recipient:
            raise ValidationError("You can't send messages to yourself")

        if not self.id:
            self.sent_at = datetime.datetime.now()
        super(Message, self).save(**kwargs)  