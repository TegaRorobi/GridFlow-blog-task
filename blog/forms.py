from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, Comment

User = get_user_model()

class RegisterForm(UserCreationForm):
	class Meta:
		model = User 
		fields = 'username', 'password1', 'password2'


class LoginForm(AuthenticationForm):
	pass
	


class PostForm(forms.ModelForm):
	class Meta:
		model = Post 
		fields = 'title', 'content'


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment 
		fields = 'content',
		widgets = {
			'content': forms.Textarea(attrs={'rows':5})
		}