from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, userProfile, Like, Following, Comments
# Register your models here.
@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'comment', 'time', 'active')
    list_filter = ('active', 'time')
    search_fields = ('post', 'user', 'comment')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active = True)
        
admin.site.register(Post)
admin.site.register(userProfile)
admin.site.register(Like)
admin.site.register(Following)