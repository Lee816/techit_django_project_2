from django.db import models

from accounts.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        ordering = ['name']  
    
    def __str__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(Category, related_name='books',on_delete=models.CASCADE)
    title = models.CharField(max_length=200,unique=True)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    summary = models.TextField()
    like = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Books_rental(models.Model):
    rental_date = models.DateField()
    return_date = models.DateField()
    book = models.ForeignKey(Book, related_name='rentals', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='rental_books', on_delete=models.CASCADE)
    book_return = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} rental "{self.book}"'
    
    
class Review(models.Model):
    GRADE = (
        (0.0, '0점'),
        (0.5, '0.5점'),
        (1.0, '1점'),
        (1.5, '1.5점'),
        (2.0, '2점'),
        (2.5, '2.5점'),
        (3.0, '3점'),
        (3.5, '3.5점'),
        (4.0, '4점'),
        (4.5, '4.5점'),
        (5.0, '5점')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    body = models.TextField(blank=True)

    grade = models.FloatField(choices=GRADE)