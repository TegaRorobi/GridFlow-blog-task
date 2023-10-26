from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.urls import reverse
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm



# Create your views here.
class PostsListView(View):
	def get(self, request, *args, **kwargs):
		posts = Post.objects.all()
		return render(request, 'blog/post-list.html', {'posts':posts})



class PostCreateUpdateView(View):
	def get(self, request, *args, **kwargs):
		create = 'id' not in kwargs
		if create:
			form = PostForm()
			return render(request, 'blog/post-create_update.html', {'form':form, 'create':True})

		post = get_object_or_404(Post, id=kwargs.get('id', 0))
		form = PostForm(instance=post)
		return render(request, 'blog/post-create_update.html', {'form':form, 'create':False})


	def post(self, request, *args, **kwargs):
		create = 'id' not in kwargs
		if create:
			form = PostForm(request.POST)
		else:
			post = get_object_or_404(Post, id=kwargs.get('id', 0))
			form = PostForm(request.POST, instance=post)
		
		if form.is_valid:
			form.save()
			return redirect(reverse('blog:posts-list'))
		messages.error('Invalid input.')
		return self.get(request)
