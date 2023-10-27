from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from .models import Post, Comment
from .forms import RegisterForm, LoginForm, PostForm, CommentForm



# Create your views here.
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
		return self.get(request, *args, **kwargs)



class LoginView(View):
	def get(self, request, *args, **kwargs):
		form = LoginForm()
		return render(request, 'blog/login.html', {'form':form})

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			print(f"username {username} password {password}")

			user = authenticate(request, username=username, password=password)
			if user is not None:
				print('USER IS VALID, LLGGING IN...')
				login(request, user)
				return redirect(reverse('blog:posts-list'))
			print('ADDING ERRORS TO THE FORM')
			form.add_error(None, "Invalid username or password")

		print('RENDERING THEE LOGIN FORM AFTER POSTT')
		return render(request, 'blog/login.html', {'form':form})



class LogoutView(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		return redirect(reverse('login'))




class PostsListView(_LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		filter_keyword = request.GET.get('filter_keyword')
		searching = None
		if filter_keyword:
			posts = Post.objects.filter(Q(title__icontains=filter_keyword)|Q(content__icontains=filter_keyword))
			searching = True
		else:
			posts = Post.objects.all()
		return render(request, 'blog/posts-list.html', {'posts':posts, 'searching':searching})



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
			ins = form.save()
			messages.success(request, "Action Successful.")
			return redirect(reverse('blog:post-retrieve', kwargs={'pk':ins.pk}))
		messages.error(request, 'Invalid input.')
		return self.get(request, *args, **kwargs)



class PostRetrieveView(_LoginRequiredMixin, View):
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



class PostDeleteView(_LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs.get('pk'))
		return render(request, 'blog/post-delete.html', {'post':post})

	def post(self, reqeust, *args, **kwargs):
		post = get_object_or_404(Post, pk=kwargs.get('pk'))
		post.delete()
		return redirect(reverse('blog:posts-list'))