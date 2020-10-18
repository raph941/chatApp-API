from rest_framework import serializers
from accounts.models import User
from chat.apps import MessagingService


class ChatUserSerializer(serializers.ModelSerializer):
    initials = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('username', 'fullname', 'initials')


class ConvPartnerSerializer(serializers.Serializer):
    id               = serializers.IntegerField()
    username         = serializers.CharField(max_length=350)
    fullname         = serializers.CharField(max_length=350)
    initials         = serializers.CharField()
    email            = serializers.EmailField()
    lastmsg          = serializers.SerializerMethodField()
    lastmsg_date     = serializers.SerializerMethodField()
    unread_count     = serializers.SerializerMethodField()

    def get_lastmsg_obj(self, obj):
        user = self.context.get('request').user
        _obj =  MessagingService.get_last_message(user, obj)
        return _obj

    def get_lastmsg(self, obj):
        return self.get_lastmsg_obj(obj).content

    def get_lastmsg_date(self, obj):
        return self.get_lastmsg_obj(obj).sent_at

    def get_unread_count(self, obj):
        user = self.context.get('request').user
        return MessagingService.get_unread_btw_users(user, obj)


class ConvMessageSerializer(serializers.Serializer):
    id                = serializers.IntegerField()
    content           = serializers.CharField()
    sender            = ChatUserSerializer()
    recipient         = ChatUserSerializer()
    sent_at           = serializers.DateTimeField()
    read_at           = serializers.DateTimeField()