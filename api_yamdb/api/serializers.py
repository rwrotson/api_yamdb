from rest_framework import serializers 
from .models import Review, Comment

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugField(source='author.username')

    def validate(self, obj):
        user - self.context['request'].user
        title = obj['title']
        if self.self
    
    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', )


class Comment