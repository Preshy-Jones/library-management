from django.shortcuts import render
from datetime import datetime, timedelta
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Book, Borrow
from datetime import datetime, timedelta

@api_view(['POST'])
def enroll_user(request):
    user = User.objects.create(
        email=request.data['email'],
        firstname=request.data['firstname'],
        lastname=request.data['lastname']
    )
    return Response({'id': user.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def book_list(request):
    books = Book.objects.filter(available=True)
    
    # Filtering
    publisher = request.query_params.get('publisher')
    category = request.query_params.get('category')
    
    if publisher:
        books = books.filter(publisher=publisher)
    if category:
        books = books.filter(category=category)
    
    return Response([{
        'id': book.id,
        'title': book.title,
        'publisher': book.publisher,
        'category': book.category
    } for book in books])

@api_view(['POST'])
def borrow_book(request):
    try:
        user = User.objects.get(email=request.data['user_email'])
        book = Book.objects.get(id=request.data['book_id'])
        
        if not book.available:
            return Response({'error': 'Book not available'}, status=status.HTTP_400_BAD_REQUEST)
        
        days = int(request.data['days'])
        due_date = datetime.now() + timedelta(days=days)
        
        Borrow.objects.create(
            user=user,
            book=book,
            due_days=days,
            due_date=due_date
        )
        
        book.available = False
        book.save()
        
        return Response({'due_date': due_date.date().isoformat()}, status=status.HTTP_201_CREATED)
    
    except (User.DoesNotExist, Book.DoesNotExist):
        return Response({'error': 'Invalid user or book'}, status=status.HTTP_404_NOT_FOUND)
