import datetime as dt
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify


class CustomUser(AbstractUser):

    class RoleChoice(models.TextChoices):
        USER = 'user', _('user')
        MODERATOR = 'moderator', _('moderator')
        ADMIN = 'admin', _('admin')

    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=50,
        choices=RoleChoice.choices,
        default=RoleChoice.USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = 'username',
    
    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.email


class CategoryAbstract(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(CategoryAbstract, self).save(*args, **kwargs)


class Category(CategoryAbstract):
    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ('pk', )


class Genre(CategoryAbstract):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('pk', )


class Title(models.Model):
    category = models.ForeignKey(
        Category, verbose_name='Категория',
        on_delete=models.PROTECT, related_name='titles'
    )
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание', blank=True, null=True)
    year = models.PositiveSmallIntegerField(
        'Год', validators=(MaxValueValidator(dt.datetime.today().year), )
    )
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ('pk', )

    def __str__(self):
        return f'{self.name} - {self.category.name}'

    @property
    def rating(self):
        rating = self.reviews.aggregate(models.Avg('score')).get('score__avg')
        return rating


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ('pk', )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ('pk', )

    def __str__(self):
        return self.text[:15]
