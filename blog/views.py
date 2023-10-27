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
		return render(request, 'blog/posts-list.html', {'posts':posts})



class PostCreateUpdateView(View):
	def get(self, request, *args, **kwargs):
		create = 'pk' not in kwargs
		if create:
			form = PostForm()
			return render(request, 'blog/post-create_update.html', {'form':form, 'create':True})

		post = get_object_or_404(Post, pk=kwargs.get('pk'))
		form = PostForm(instance=post)
		return render(request, 'blog/post-create_update.html', {'form':form, 'create':False})


	def post(self, request, *args, **kwargs):
		create = 'pk' not in kwargs
		if create:
			form = PostForm(request.POST)
		else:
			post = get_object_or_404(Post, pk=kwargs.get('pk'))
			form = PostForm(request.POST, instance=post)

		if form.is_valid:
			form.save()
			messages.success(request, "Action Successful.")
			return redirect(reverse('blog:posts-list'))
		messages.error(request, 'Invalid input.')
		return self.get(request, *args, **kwargs)



class PostRetrieveView(View):
	def get(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs.get('pk'))
		form = CommentForm()
		return render(request, 'blog/post-retrieve.html', {'post':post, 'form':form})

	def post(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs.get('pk'))
		form = CommentForm(request.POST)
		if form.is_valid():
			ins = form.save(commit=False)
			ins.user = request.user
			ins.post = post
			ins.save()
			messages.success(request, 'Comment successfully added')
		else:
			messages.error(request, 'Invalid input.')
		return self.get(request, *args, **kwargs)



class PostDeleteView(View):
	def get(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs.get('pk'))
		return render(request, 'blog/post-delete.html', {'post':post})

	def post(self, reqeust, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs.get('pk'))
		post.delete()
		return redirect(reverse('blog:posts-list'))