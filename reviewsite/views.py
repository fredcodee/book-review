from django import forms
from django.urls.base import is_valid_path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from .models import *
from .forms import Bookimageform
import random


# Create your views here.

#views
def index(request):
  #get user group
  group  = request.user.groups.all()[0].name
  context = {
    'get_books' : Book.objects.all()[:3],
    'group': group   
  }
  return render(request,'base.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Author'])
def add_book(request):
  if request.method == 'POST':
    title = request.POST['title']
    summary  = request.POST['summary']
    
    #create new book id
    book_isbn = random.randint(1,1000)
    #check if id exists
    while Book.objects.filter(book_isbn = book_isbn):
      book_id  = random.randint(1,1000)
    
    try:
      new_book = Book(title = title.title(), book_isbn = book_isbn, summary = summary,author = request.user)
      new_book.save()
    except:
      messages.error(request, 'cant upload this book')
      return redirect('add_book')
    
    messages.success(request, 'book uploaded successfully, you can now upload the book cover')
    return redirect('edit_book', book_id = new_book.id)
     
  
  return render(request, 'addbook.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Author'])
def edit_book(request, book_id):
  get_book = Book.objects.get(pk = book_id)
  form  = Bookimageform(instance=get_book)
  if request.method == "POST":
    form = Bookimageform(request.POST,request.FILES,instance=get_book)
    if form.is_valid():
      form.save()
  
  context  = {
    'get_book' : get_book,
    'form':form
  
  }
  
  return render(request,'editbook.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Author'])
def my_books(request):
  my_books = Book.objects.filter(author = request.user).all()
  
  context = {
    'books':my_books
  }
  
  return render(request, 'mybooks.html', context)
  

@login_required(login_url='login')
@allowed_users(allowed_roles=['Author'])
def delete_book(request, book_id):
  book = Book.objects.get(pk = book_id)
  book.delete()
  messages.success(request,'Book Deleted')
  return redirect('my_books')


def bookpage(request, book_id):
  get_book = Book.objects.get(pk = book_id)
  context = {
    'book':get_book,
    'total_likes': get_book.total_likes,
    'total_dislikes':get_book.total_dislikes,
    'reviews':Reviews.objects.filter(book =get_book).order_by('-date_posted')
  }
  
  return render(request, 'bookpage.html', context)
  
@login_required(login_url='login')
def like_book(request, book_id):
  book = get_object_or_404(Book, id = request.POST.get('book_id'))
  if book.dislikes.filter(id = request.user.id).exists():
    book.dislikes.remove(request.user)   
  
  book.likes.add(request.user)
  return redirect('bookpage', book_id = book.id)

@login_required(login_url='login')
def dislike_book(request, book_id):
  book  = get_object_or_404(Book, id = request.POST.get('book_id'))
  
  #check if user has liked the book and remove
  if book.likes.filter(id=request.user.id).exists():
    book.likes.remove(request.user)
  
  book.dislikes.add(request.user)
  return redirect('bookpage', book_id = book.id)
    
    
@login_required(login_url='login')
def add_review(request, book_id):
  book = get_object_or_404(Book, id = book_id)
  comment  = request.POST.get('comment')
  
  try:
    new_review  = Reviews(book = book, user_id = request.user, comment = comment)
    new_review.save()
  except:
    messages.error(request, 'Sorry cant comment on this book try again later')
    return redirect('bookpage', book_id = book.id)
    
  messages.success(request, f'you just commented on {book.title}')
  return redirect('bookpage', book_id = book.id)
  
  
  
@login_required(login_url='login')
def delete_review(request, review_id):
  review  = get_object_or_404(Reviews, id = review_id)
  if review.user_id == request.user:
    review.delete()
    messages.success(request, 'review deleted')
    return redirect ('bookpage', book_id = review.book.id)
    
  

def search(request):
  if request.method == 'POST':
    name = request.POST['search']
    if name:
      output = Book.objects.filter(title__startswith = name.title()) or Book.objects.filter( author__username =  name).all()
    else:
      messages.success(request, f'error!, try again later')
      return redirect(request, 'home')

    return render(request, 'view_search.html', context={'output': output})

    



