from rest_framework import serializers
from accounts.models import User
from chat.apps import MessagingService


class ChatUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'fullname', 'image_url',)


class ConvPartnerSerializer(serializers.Serializer):
    id               = serializers.IntegerField()
    username         = serializers.CharField(max_length=350)
    fullname         = serializers.CharField(max_length=350)
    image_url        = serializers.CharField()
    email            = serializers.EmailField()
    lastmsg          = serializers.SerializerMethodField()
    lastmsg_date     = serializers.SerializerMethodField()
    unread_count     = serializers.SerializerMethodField()

    def get_lastmsg_obj(self, obj):
        user = self.context.get('request').user
        _obj =  MessagingService.get_last_message(user, obj)
        return _obj

    def get_lastmsg(self, obj):
        # import pdb ; pdb.set_trace()
        return self.get_lastmsg_obj(obj).content

    def get_lastmsg_date(self, obj):
        return self.get_lastmsg_obj(obj).sent_at

    def get_unread_count(self, obj):
        user = self.context.get('request').user
        # import pdb ; pdb.set_trace()
        return MessagingService.get_unread_btw_users(user, obj)


class ConvMessageSerializer(serializers.Serializer):
    id                = serializers.IntegerField()
    content           = serializers.CharField()
    sender            = ChatUserSerializer()
    recipient         = ChatUserSerializer()
    sent_at           = serializers.DateTimeField()
    read_at           = serializers.DateTimeField()