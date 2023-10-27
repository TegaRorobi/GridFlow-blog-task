from django.contrib import admin
from .models import Post, Comment 

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	model = Post 
	list_display = 'title', 'content', 'created_at', 'updated_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	model = Comment 
	list_display = 'user', 'post', '_content', 'created_at', 'updated_at'

	@admin.display()
	def _content(self, obj):
		content = obj.content
		return content if len(content) <= 20 else content[:40]+'...'