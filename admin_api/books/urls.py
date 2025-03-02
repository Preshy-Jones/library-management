from django.urls import path
from . import views

urlpatterns = [
    # Books
    path('books/', views.book_list_create, name='book-list-create'),
    path('books/<int:pk>/', views.book_delete, name='book-delete'),
    
    # Users
    path('users/', views.user_list, name='user-list'),
    
    # Borrows
    path('borrows/', views.borrow_list, name='borrow-list'),
]