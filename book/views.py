from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Book, Category
from .forms import SearchForm
from django.db.models import Q
from cart.models import *


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


class SearchView(ListView):
    model = Book
    template_name = 'search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Book.objects.filter(
                Q(name__icontains=query) | Q(category__name__icontains=query) | Q(author__icontains=query))
            result = postresult
        else:
            result = None
        return result
