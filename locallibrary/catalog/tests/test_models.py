from django.test import TestCase
from ..models import Author, Genre, Book, BookInstance


# Create your tests here.

class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Настройка не модифицированных объектов, используемых всеми методами тестирования
        Author.objects.create(first_name='Александр', last_name='Пушкин')

    def test_first_name_label(self):
        # Получение объекта для тестирования
        author = Author.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = author._meta.get_field('first_name').verbose_name
        # Сравнить значение с ожидаемым результатом
        self.assertEquals(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # Это также не удастся, если urlconf не определен.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')


class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Настройка не модифицированных объектов, используемых всеми методами тестирования
        Genre.objects.create(name='Драма')

    def genre_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_object_name(self):
        genre = Genre.objects.get(id=1)
        expected_object_name = genre.name
        self.assertEquals(expected_object_name, str(genre))


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Настройка не модифицированных объектов, используемых всеми методами тестирования
        Book.objects.create(title='Мёртвые души', summary='Книга о мёртвых душах', isbn='9780393952926')

    def test_title_max_length(self):
        title = Book.objects.get(id=1)
        max_length = title._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_summary_max_length(self):
        summary = Book.objects.get(id=1)
        max_length = summary._meta.get_field('summary').max_length
        self.assertEquals(max_length, 1000)

    def test_isbn_label(self):
        isbn = Book.objects.get(id=1)
        field_label = isbn._meta.get_field('isbn').verbose_name
        self.assertEquals(field_label, 'isbn')

    def test_isbn_max_length(self):
        isbn = Book.objects.get(id=1)
        max_length = isbn._meta.get_field('isbn').max_length
        self.assertEquals(max_length, 13)

    def test_object_book(self):
        book = Book.objects.get(id=1)
        expected_object_name = book.title
        self.assertEquals(expected_object_name, str(book))

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        # Это также не удастся, если urlconf не определен.
        self.assertEquals(book.get_absolute_url(), '/catalog/book/1')