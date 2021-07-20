from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CustomUser, Review, Comment


class EmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    
    class Meta:
        fields = ['email']
        model = CustomUser


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ['first_name', 'last_name', 'username', 'bio',
                  'email', 'role']
        model = CustomUser


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', )

    def validate(self, data):
        user = self.context['request'].user
        title = data['title']
        if self.context['request'].method == 'POST':
            if Review.objects.get(title=title, author=user).exists():
                raise ValidationError('You have already left your review!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', )
