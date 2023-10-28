from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.views.generic import View
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q, Count
from .models import Post, Comment
from .forms import RegisterForm, LoginForm, PostForm, CommentForm


class _LoginRequiredMixin(LoginRequiredMixin):
	login_url = '/accounts/login/'



class RegisterView(View):

	def get(self, request, *args, **kwargs):
		form = RegisterForm()
		return render(request, 'blog/register.html', {'form':form})

	def post(self, request, *args, **kwargs):
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Action Successful.")
			return redirect(reverse('blog:posts-list'))
		messages.error(request, 'Invalid input.')
		return render(request, 'blog/register.html', {'form':form})



class LoginView(View):

	def get(self, request, *args, **kwargs):
		form = LoginForm()
		return render(request, 'blog/login.html', {'form':form})

	def post(self, request, *args, **kwargs):
		form = LoginForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect(reverse('blog:posts-list'))
		return render(request, 'blog/login.html', {'form':form})



class LogoutView(_LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return render(request, 'blog/logout.html', {})

	def post(self, request, *args, **kwargs):
		logout(request)
		return redirect(reverse('blog:posts-list'))



class PostsListView(View):

	def get(self, request, *args, **kwargs):
		filter_keyword = request.GET.get('filter_keyword')
		searching = None
		if filter_keyword:
			posts = Post.objects.filter(Q(title__icontains=filter_keyword)|Q(content__icontains=filter_keyword))
			searching = True
		else:
			posts = Post.objects.all()

		try:
			page_size = int(request.GET.get('page_size', 10))
		except:
			page_size=10

		paginator = Paginator(posts, page_size)

		try:
			page_number = int(request.GET.get('page', 1))
		except:
			page_number = 1

		page_number = max(1, min(page_number, paginator.num_pages))

		posts = paginator.page(page_number)

		return render(request, 'blog/posts-list.html', {'posts':posts, 'paginator':paginator, 'searching':searching})



class PostCreateUpdateView(_LoginRequiredMixin, View):

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
			ins = form.save(commit=False)
			if create:
				ins.author = request.user 
				ins.save()
			messages.success(request, "Action Successful.")
			return redirect(reverse('blog:post-retrieve', kwargs={'pk':ins.pk}))
		messages.error(request, 'Invalid input.')
		return self.get(request, *args, **kwargs)



class PostRetrieveView(View):

	def get(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs.get('pk'))
		form = CommentForm()

		queryset = post.comments.all()
		try:
			page_size = int(request.GET.get('page_size', 5))
		except:
			page_size=5

		# if the comments aren't even up to the page size, then there's no need to set up a paginator
		# we can also get this information without making another query to the database hence the aggregation.
		if queryset.aggregate(_total_count=Count('*'))['_total_count'] < page_size:
			return render(request, 'blog/post-retrieve.html', {'post':post, 'post_comments':queryset, 'form':form})

		paginator = Paginator(queryset, page_size)
		try:
			page_number = int(request.GET.get('page', 1))
		except:
			page_number = 1
		page_number = max(1, min(page_number, paginator.num_pages))

		post_comments = paginator.page(page_number)
		return render(request, 'blog/post-retrieve.html', {'post':post, 'post_comments':post_comments, 'paginator':paginator, 'form':form})
		

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



class PostDeleteView(_LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs.get('pk'))
		return render(request, 'blog/post-delete.html', {'post':post})

	def post(self, reqeust, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs.get('pk'))
		post.delete()
		return redirect(reverse('blog:posts-list'))