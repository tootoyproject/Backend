from .views import PostsDetail, PostsList
from django.urls import path

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>/', PostsDetail.as_view()),
]