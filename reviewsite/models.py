from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Book(models.Model):
  title = models.CharField(max_length=99, null= True)
  book_isbn = models.IntegerField()
  summary = models.TextField(max_length=1000, null= True)
  date_posted = models.DateTimeField(default=timezone.now, null= True)
  author = models.ForeignKey(
      User, on_delete=models.CASCADE, null= True)
  image = models.ImageField(default = 'images/books/default.png',upload_to='images/books', blank = True)
  likes = models.ManyToManyField(User, related_name='book_likes')
  dislikes = models.ManyToManyField(User, related_name='book_dislikes')

  def __str__(self):
    return self.title
  
  def total_likes(self):
    return self.likes.count()
  
  def total_dislikes(self):
    return self.dislikes.count()
  
  
  

#reviews
class Reviews(models.Model):
  date_posted = models.DateTimeField(default=timezone.now ,null= True)
  user_id = models.ForeignKey(User, on_delete = models.CASCADE , null= True)
  book = models.ForeignKey(Book, on_delete=models.CASCADE, null= True)
  comment = models.CharField(max_length= 300)
  
  
  def total_review(self):
    return self.comment.count()
  
