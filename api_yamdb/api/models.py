from django.db import models

class Review(models.Model):
    title = models.ForeignKey( 
        Title, on_delete=models.CASCADE, related_name='reviews' 
    )
    text = models.TextField() 
    author = models.ForeignKey( 
        User, on_delete=models.CASCADE, related_name='reviews' 
    ) 
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField( 
        'Дата публикации', auto_now_add=True 
    )
    
    def __str__(self):
        return self.text[:15]

class Comment(models.Model):
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments' 
    )
    text = models.TextField()
    author = models.ForeignKey( 
        User, on_delete=models.CASCADE, related_name='reviews' 
    )
    pub_date = models.DateTimeField( 
        'Дата публикации', auto_now_add=True 
    )

    def __str__(self):
        return self.text[:15]