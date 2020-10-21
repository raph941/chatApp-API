from __future__ import unicode_literals

from .models import Message, ChatRoom
from accounts.models import User
from .signals import message_read, message_sent
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


class MessagingService(object):
    """
    A object to manage all messages and conversations
    """

    # Message creation
    def send_message(self, sender, recipient, message):
        """
        Send a new message
        :param sender: user
        :param recipient: user
        :param message: String
        :return: Message and status code
        """
        logger.info('MessagingService: SENDING NEW MESSAGE')
        if sender == recipient:
            raise ValidationError("You can't send messages to yourself.")

        if type(sender) == int and type(recipient) == int:
            sender = User.objects.get(pk=sender)
            recipient = User.objects.get(pk=recipient)
        room, created = ChatRoom.objects.get_or_new(sender, recipient)

        message = Message(sender=sender, recipient=recipient, content=str(message), room=room)
        message.save()

        message_sent.send(sender=message, from_user=message.sender, to=message.recipient)

        # The second value acts as a status value
        return message, 200

    # Message reading
    def get_unread_messages(self, user):
        """
        List of unread messages for a specific user
        :param user: user
        :return: messages
        """
        logger.info('MessagingService: GETTING UNREAD MESSAGES')
        return Message.objects.all().filter(recipient=user, read_at=None)

    def get_unread_btw_users(self, user1, user2):
        """
        Number of unread messages between two users
        e.g a user gets the number of unread messages he has recived from another user
        :param user1, user2: User
        """
        logger.info('MessagingService: FETCHING THE NUMBER OF UNREAD MESSAGES BETWEEN TWO USERS')
        count = Message.objects.filter(sender=user2, recipient=user1, read_at=None).count()
        return count


    def read_message(self, message_id):
        """
        Read specific message
        :param message_id: Integer
        :return: Message Text
        """
        logger.info('MessagingService: MARK SPECIFIC MESSAGE AS READ')
        try:
            message = Message.objects.get(id=message_id)
            self.mark_as_read(message)
            return message.content
        except Message.DoesNotExist:
            return ""

    def read_message_formatted(self, message_id):
        """
        Read a message in the format <User>: <Message>
        :param message_id: Id
        :return: Formatted Message Text
        """
        logger.info('MessagingService: FORMART MESSAGE')
        try:
            message = Message.objects.get(id=message_id)
            self.mark_as_read(message)
            return message.sender.username + ": "+message.content
        except Message.DoesNotExist:
            return ""

    # Conversation management

    def get_conversations(self, user):
        """
        Lists all conversation-partners for a specific user
        :param user: User
        :return: Conversation list
        """
        logger.info('MessagingService: GETTING ALL CONVERSATION PARTNERS FOR SPECIFIC USER')
        if type(user) == int:
            user = User.objects.get(pk=user)

        all_conversations = Message.objects.all().filter(Q(sender=user) | Q(recipient=user))

        contacts = []
        for conversation in all_conversations:
            if conversation.sender != user:
                contacts.append(conversation.sender)
            elif conversation.recipient != user:
                contacts.append(conversation.recipient)

        # To abolish duplicates
        return list(set(contacts))

    #conversation room
    def get_conversation_room(self, user1, user2):
        """
        Chat room for two users
        user1 : int or object
        user2 : int or object
        """
        logger.info('MessagingService: GETTING CONVERSATION ROOM FOR TWO USERS')
        if type(user1) == int and type(user2) == int:
            u1 = User.objects.get(pk=user1)
            u2 = User.objects.get(pk=user2)
            users = [ u1, u2 ]
        else: users = [user1, user2]

        room = ChatRoom.objects.all().filter(first__in=users, second__in=users)[0]
        return room
    

    def get_conversation(self, user1, user2, limit=50, reversed=False):
        """
        List of messages between two users
        :param user1: User
        :param user2: User
        :param limit: int
        :param reversed: Boolean - Makes the newest message be at index 0
        :return: messages
        """
        logger.info('MessagingService: GETTING CONVERSATION MESSAGES')
        users = [user1, user2]

        # Newest message first if it's reversed (index 0)
        if reversed:
            order = '-pk'
        else:
            order = 'pk'

        conversation = Message.objects.filter(sender__in=users, recipient__in=users).order_by(order)

        for message in conversation:
            if message.sender==user2 and message.read_at==None:
                self.mark_as_read(message)

        if len(conversation) > limit:
            starting_point = len(conversation) - limit
            conversation = conversation[starting_point:]

        return conversation

    # Helper methods
    def mark_as_read(self, message):
        """
        Marks a message as read, if it hasn't been read before
        :param message: Message
        """
        logger.info('MessagingService: MARK MESSAGE OBJECT AS READ')
        if message.read_at is None:
            message.read_at = timezone.now()
            message_read.send(sender=message, from_user=message.sender, to=message.recipient)
            message.save()

    def get_last_message(self, user1, user2):
        """
        Get the last message instance between two chating parties
        :param user1: User
        :param user2: User
        """
        logger.info('MessagingService: GETTING LAST MESSAGE BETWEEN TWO USERS')
        users = [user1, user2]
        conversation = Message.objects.all().filter(sender__in=users, recipient__in=users)
        return conversation.last()