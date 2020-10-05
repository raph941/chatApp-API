from .models import Message, ChatRoom
from django.contrib import admin

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('id', 'sender', 'content', )

admin.site.register(Message, MessageAdmin)

class ChatRoomAdmin(admin.ModelAdmin):
    model = ChatRoom
    list_display = ('id', 'first', 'second', 'timestamp',)

admin.site.register(ChatRoom, ChatRoomAdmin)