from django.db import models
from django.contrib.auth.models import User
from src.utils import shorten

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()

	# timestamps
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title 


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	blog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

	content = models.TextField()

	# timestamps
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		content = self.content
		return content if len(content) <= 20 else content[:20]+'...'