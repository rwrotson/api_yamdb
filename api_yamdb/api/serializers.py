from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CustomUser, Review, Comment
from .models import Category, Title, Genre


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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre', 'rating')


class TitleCreateSerializer(TitleSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    title = TitleSerializer()

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title', )

    def validate(self, data):
        user = self.context['request'].user
        title = data['title']
        if self.context['request'].method == 'POST':
            if Review.objects.get(title=title, author=user).exists():
                raise ValidationError('You have already left your review!')
        return data


class ReviewCreateSerializer(ReviewSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.SlugRelatedField(
        slug_field='slug', queryset=Title.objects.all()
    )


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    review = ReviewSerializer()

    class Meta:
        fields = ('id', 'review', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('review', )


class CommentCreateSerializer(CommentSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        slug_field='slug', queryset=Review.objects.all()
    )
