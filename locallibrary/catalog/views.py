from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.
    num_genre = Genre.objects.count()
    num_book = Book.objects.filter(title__icontains='Тарас Бульба').count()
    # Количество посещений этого представления, подсчитанное в переменной сеанса.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Визуализация HTML-шаблона index.html с данными в контекстной переменной.
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_genre': num_genre, 'num_book': num_book, 'num_visits': num_visits},  # num_visits appended
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    context_object_name = 'book_list'  # ваше собственное имя переменной контекста в шаблоне
    template_name = 'books/book_list.html'  # Определение имени вашего шаблона и его расположения

    def get_queryset(self):
        return Book.objects.filter(title__icontains='')  # [:5]  # Получить 5 книг, содержащих 'war' в заголовке

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2
    context_object_name = 'author_list'  # ваше собственное имя переменной контекста в шаблоне
    template_name = 'authors/author_list.html'  # Определение имени вашего шаблона и его расположения

    def get_queryset(self):
        # return Author.objects.filter(last_name__icontains='')  # [:5]  # Получить 5 книг, содержащих 'war' в заголовке
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = 'This is just some data'
        return context


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Общее представление на основе класса, в котором перечислены книги, предоставленные текущему пользователю.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
