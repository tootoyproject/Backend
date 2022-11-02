from rest_framework import viewsets
from .serializers import PostsSerializer
from .models import Posts

class PostsViewSet(viewsets.ModelViewSet):
   queryset = Posts.objects.all()
   serializer_class = PostsSerializer
