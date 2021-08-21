from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Book, Category


# Create your views here.

class BookListView(ListView):
    model = Book
    queryset = Book.objects.all()
    template_name = 'list_book.html'


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_Detail.html'


class BookCreateView(CreateView):
    model = Book
    template_name = 'Book_Create.html'
    fields = ('name', 'description', 'author', 'date_created', 'Inventory', 'price')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_list.html'

    # def get_queryset(self):
    #     obj = {'queryset': Book.objects.religious(),
    #            'queryset1': Book.objects.novel(),
    #            'queryset2': Book.objects.educational(),
    #            }
    #     return obj
