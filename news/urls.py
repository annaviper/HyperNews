from django.urls import path, include
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('news/', views.news, name='news'),
	path('news/<int:target>/', views.article, name='article'),
	path('news/create/', views.create_article, name='create')
]
