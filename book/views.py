from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Book, Category
from .forms import SearchForm
from django.db.models import Q
from cart.models import *
from orders.models import ShoppingCart


# Create your views here.

class BookListView(ListView):
    model = Book
    queryset = Book.objects.all()
    template_name = 'list_book.html'


# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'book_Detail.html'
def book_detail(request, id):
    book = Book.objects.get(id=id)
    if book.favorite.filter(id=request.user.id).exists():
        book.is_favorite = True
    return render(request, 'book_Detail.html', {'book': book})


def favorite_book(request, id):
    url = request.META.get('HTTP_REFERER')
    book = Book.objects.get(id=id)
    # book.is_favorite = False
    if book.favorite.filter(id=request.user.id).exists():
        book.favorite.remove(request.user)
        book.is_favorite = False
    else:
        book.favorite.add(request.user)
        book.is_favorite = True
    book.save()
    return redirect(url)

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


def category(request):
    category = Category.objects.all()
    return render(request, 'list_book.html', {'category': category})



