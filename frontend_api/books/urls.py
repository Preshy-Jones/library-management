from django.urls import path
from . import views

urlpatterns = [
    path('enroll/', views.enroll_user, name='enroll-user'),
    path('books/', views.book_list, name='book-list'),
    path('borrow/', views.borrow_book, name='borrow-book'),
]