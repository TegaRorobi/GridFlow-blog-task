from django.urls import re_path
from .views import (
	PostsListView, 
	PostCreateUpdateView,
	PostRetrieveView,
	PostDeleteView
)

app_name = 'blog'
urlpatterns = [
	re_path('^list[-_]?(posts)?/?$', PostsListView.as_view(), name='posts-list'),
	re_path('^create[-_]?(post)?/?$', PostCreateUpdateView.as_view(), name='post-create'),
	re_path('^update[-_]?(post)?/(?P<pk>\d+)/?$', PostCreateUpdateView.as_view(), name='post-update'),
	re_path('^retrieve[-_]?(post)?/(?P<pk>\d+)/?$', PostRetrieveView.as_view(), name='post-retrieve'),
	re_path('^delete[-_]?(post)?/(?P<pk>\d+)/?$', PostDeleteView.as_view(), name='post-delete'),
]