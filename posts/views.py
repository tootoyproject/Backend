from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import HttpResponse
from django.http import Http404
from .serializers import PostsSerializer
from .models import Posts
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class PostsViewSet(viewsets.ModelViewSet):
   queryset = Posts.objects.all()
   serializer_class = PostsSerializer

class PostsList(APIView):
   def get(self, request):
      posts = Posts.objects.all()
      serializer = PostsSerializer(posts, many=True)
      return Response(serializer.data)
   
   def post(self, request):
      serializer = PostsSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostsDetail(APIView):
   def get_object(self, pk):
      try:
         return Posts.objects.get(pk=pk)
      except Posts.DoesNotExist:
         raise Http404
   
   def get(self, request, pk):
      posts = self.get_object(pk)
      serializer = PostsSerializer(posts)
      return Response(serializer.data)
   
   def put(self, request, pk):
      channel_layer = get_channel_layer()
      posts = self.get_object(pk)
      serializer = PostsSerializer(posts, data=request.data)
      if serializer.is_valid():
         serializer.save()
         async_to_sync(channel_layer.group_send)("Posts", {"type": "Posts.system_message", "text": "불가"})
         return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED, )
   
   def delete(self, request, pk):
      posts = self.get_object(pk)
      posts.delete()
      return Response(data={"detail":"성공"},status=status.HTTP_204_NO_CONTENT)