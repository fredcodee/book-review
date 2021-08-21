from django.urls import path
from . import views


urlpatterns = [
  path('', views.index, name = 'home'),
  path('book/add', views.add_book, name = 'add_book'),
  path('book/delete', views.delete_book, name = 'delete_book'),
  path('book/edit/<int:book_id>', views.edit_book, name = 'edit_book'),
  path('books/mybooks', views.my_books, name= 'my_books'),
  path('book/view/<int:book_id>', views.bookpage, name= 'bookpage'),
  path('book/delete/mybooks/<int:book_id>', views.delete_book, name='delete_book'),
  path('book/like/<int:book_id>', views.like_book, name= 'like_book'),
  path('book/dislike/<int:book_id>', views.dislike_book, name= 'dislike_book'),
  path('book/review/<int:book_id>', views.add_review, name= 'add_review'),
  path('book/review/delete/<int:review_id>', views.delete_review, name = 'delete_review'),
  path('search', views.search, name = 'search')
  
]
