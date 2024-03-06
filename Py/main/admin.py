from django.contrib import admin
from .models import CustomUser, Room, Message, Course, Inst_info, Course_Application,Payment, Migrant, Property

admin.site.register(CustomUser)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Course)
admin.site.register(Inst_info)
admin.site.register(Course_Application)
admin.site.register(Payment)
admin.site.register(Migrant)
admin.site.register(Property)




from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Thread,ChatMessage

admin.site.register(ChatMessage)


class ChatMessage(admin.TabularInline):
    model = ChatMessage


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)