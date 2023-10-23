from django.contrib import admin
from .models import CustomUser, Room, Message, Course, Inst_info, Course_Application,Payment, Migrant

admin.site.register(CustomUser)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Course)
admin.site.register(Inst_info)
admin.site.register(Course_Application)
admin.site.register(Payment)
admin.site.register(Migrant)


