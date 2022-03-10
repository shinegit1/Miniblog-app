from django.contrib import admin
from .models import Post, Contact

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display =['id','title','descript']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
  list_display = ['id','first_name','last_name','email','subject','message']
