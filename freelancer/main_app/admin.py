from django.contrib import admin
from .models import Profile, Job, Category, RequestToClient, Notification

# Register your models here.
admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Category)
admin.site.register(RequestToClient)
admin.site.register(Notification)