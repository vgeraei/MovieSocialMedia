from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(myUser)
admin.site.register(Movie)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(RoleTable)