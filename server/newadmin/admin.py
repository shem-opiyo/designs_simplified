from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(AdminUser) 
admin.site.register(Project) 
admin.site.register(ImagesAlbum)
admin.site.register(Image)
admin.site.register(ProjectsManager)