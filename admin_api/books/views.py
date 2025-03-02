from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book, User, Borrow


@api_view(['GET', 'POST'])
def book_list_create(request):
    """Handle book creation and listing"""
    if request.method == 'GET':
        books = Book.objects.all()
        return Response([{
            'id': book.id,
            'title': book.title,
            'publisher': book.publisher,
            'category': book.category
        } for book in books])
    
    elif request.method == 'POST':
        book = Book.objects.create(
            title=request.data['title'],
            publisher=request.data['publisher'],
            category=request.data['category']
        )
        return Response({'id': book.id}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def book_delete(request, pk):
    """Delete a specific book"""
    try:
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def user_list(request):
    """List all enrolled users"""
    users = User.objects.all()
    return Response([{
        'id': user.id,
        'email': user.email,
        'firstname': user.firstname,
        'lastname': user.lastname
    } for user in users])

@api_view(['GET'])
def borrow_list(request):
    """List all book borrows"""
    borrows = Borrow.objects.all()
    return Response([{
        'id': borrow.id,
        'user_id': borrow.user.id,
        'book_id': borrow.book.id,
        'borrowed_date': borrow.borrowed_date,
        'due_date': borrow.due_date
    } for borrow in borrows])