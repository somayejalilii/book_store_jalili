from django.urls import path

from book.views import *

app_name = 'book'

urlpatterns = [
    path('book_list/', BookListView.as_view(), name='list'),
    path('book_detail/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book_create/', BookCreateView.as_view(), name='book_create'),
    path('category_detail/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('feed/', SearchView.as_view(), name='search_bar'),
]
