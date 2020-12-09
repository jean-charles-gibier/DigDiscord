from django.contrib import admin
from .models import Channel, Link as Lnk, Message, ModelReference, Server, User

# Register your models here.

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    pass

@admin.register(Lnk)
class LnkAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(ModelReference)
class ModelReferenceAdmin(admin.ModelAdmin):
    pass

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass