from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Book, Category
from .forms import SearchForm
from django.db.models import Q,Max,Min
from cart.models import *
from orders.models import ShoppingCart
from django.core.mail import EmailMessage
from django.contrib import messages
from .filters import BookFilter


# Create your views here.

# class BookListView(ListView):
#     """
#     جهت لیست کردن محصولات با استفاده از لیست ویو جنگو
#     """
#     model = Book
#     queryset = Book.objects.all()
#     template_name = 'list_book.html'


def all_product(request):
    books = Book.objects.all()
    product = Book.objects.all()
    # min = Book.objects.aggregate(price=Min('price'))
    # min_price = int(min('price'))
    # max = Book.objects.aggregate(price=Max('price'))
    # max_price = int(max('price'))
    filter = BookFilter(request.GET, queryset=books)
    books = filter.qs
    return render(request, 'list_book.html', {'product':product,'books': books, 'filter': filter})


# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'book_Detail.html'
def book_detail(request, id):
    """
    جزییات محصول
    :param request:
    :param id:
    :return:
    """
    book = Book.objects.get(id=id)
    if book.favorite.filter(id=request.user.id).exists():
        book.is_favorite = True
    return render(request, 'book_Detail.html', {'book': book})


def favorite_book(request, id):
    """
    در صورت لایک توسط کاربر اضافه کردن محصول به لیست
    علاقه مندی های کاربر
    تغییر فیلد علاقه مندی از False به True
    :param request:
    :param id:
    :return:
    """
    url = request.META.get('HTTP_REFERER')
    print('salam', id)
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
    """
    چزییات محصول و موضوع کتاب
    """
    model = Category
    template_name = 'category_list.html'


class SearchView(ListView):
    """
    سرچ بار
    """
    model = Book
    template_name = 'search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        """
        سرچ روی نام کتاب نام نویسنده و موضوع کتاب
        امکان سرچ بصورت کلمه ای
        :return:
        """
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


def contact(request):
    """
    صفحه ارتباط با ما که پیام مشتری به ایمیل ادمین ارسال میشود
    :param request:
    :return:
    """
    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        msg = request.POST['message']
        body = subject + '\n' + email + '\n' + msg
        form = EmailMessage(
            'ارتباط با ما',
            body,
            'test',
            ('s68jalili@gmail.com',),
        )
        form.send(fail_silently=False)
        messages.success(request, 'پیام شما با موفقیت ارسال شد')
    return render(request, 'contact.html')
