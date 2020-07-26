from django.urls import path
from . import views
from .views import search_user

urlpatterns = [
    path('', views.userhome, name='userhome'),
    path('post',views.post, name='post'),
    path('like',views.likepost, name="likepost"),
    path('<int:postId>', views.delpost, name="delpost"),
    path('<str:username>',views.Profile, name="Profile"),
    path("comment/<int:PostId>", views.comment, name="comment"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("search/",search_user.as_view(),name="search"),
]