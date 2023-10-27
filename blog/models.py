from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()

	# timestamps
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return reverse('blog:post-retrieve', kwargs={'pk':self.pk})

	def __str__(self):
		return self.title 


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

	content = models.TextField()

	# timestamps
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		content = self.content
		return content if len(content) <= 20 else content[:20]+'...'
