from .models import Book

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        book_id = self.cart.keys()
        books = Book.objects.filter(id__in=book_id)
        cart = self.cart.copy()
        for book in books:
            cart[str(book.id)]['book'] = book

        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def get_total_price(self):
        return sum(int(i['price']) * i['quantity'] for i in self.cart.values())

    def remove(self, book):
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def add(self, book, quantity):
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': 0, 'price': str(book.price)}
        self.cart[book_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()
