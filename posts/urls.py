from django.urls import path, include
import views

urlpatterns = [
    path('',include('api.urls')),
    path('/posts', views.PostsList.as_view()),
]