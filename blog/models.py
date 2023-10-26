from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()

	# timestamps
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)



class Comment(models.Model):
	blog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

	content = models.TextField()

	# timestamps
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)