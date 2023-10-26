from django.urls import re_path
from .views import PostsListView, PostCreateUpdateView

app_name = 'blog'

urlpatterns = [
	re_path('^list[-_]?(posts)?/?$', PostsListView.as_view(), name='posts-list'),
	re_path('^create[-_]?(post)?/?$', PostCreateUpdateView.as_view(), name='post-create'),
	re_path('^update[-_]?(post)?/(?P<id>\d+)/?$', PostCreateUpdateView.as_view(), name='post-update'),
]