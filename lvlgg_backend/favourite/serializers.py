from rest_framework import serializers
from .models import Favourite

class FavouriteSerializer(serializers.ModelSerializer):
    blog_id = serializers.IntegerField(source='blog.id')
    blog_title = serializers.CharField(source='blog.title')
    blog_game = serializers.CharField(source='blog.game')

    class Meta:
        model = Favourite
        fields = ('blog_id', 'blog_title', 'blog_game')
