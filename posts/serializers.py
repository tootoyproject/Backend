from rest_framework import serializers
from .models import Posts

class PostsSerializer(serializers.ModelSerializer) :
        class Meta:
            model = Posts
            fields = ['postid', 'title', 'content']
            
    # postid = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(max_length=200)
    # content = serializers.TextField()

    # def create(self, validated_data):
    #     return Posts.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.data.get('title', instance.title)
    #     instance.content = validated_data.data.get('content', instance.content)
    #     instance.save()
    #     return instance