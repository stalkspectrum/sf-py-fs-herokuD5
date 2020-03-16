from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from p_library.models import Author, Book, Publisher, Reader
from p_library.forms import AuthorForm, BookForm

class AuthorList(ListView):
    model = Author
    template_name = 'authors_list.html'

class AuthorEdit(CreateView):
    model = Author
    form_class = AuthorForm
    #success_url = reverse_lazy('p_library:authors_list')
    success_url = reverse_lazy('authors_list')
    template_name = 'authors_edit.html'

def index(request):
    template = loader.get_template('index.html')
    books = Book.objects.all()
    books_count = books.count()
    numbers = [ str(x) for x in range(1, 101) ]
    biblio_data = {
        'title': 'мою библиотеку',
        'books': books,
        'numbers': numbers,
    }
    return HttpResponse(template.render(biblio_data, request))

def author_create_many(request):
    ''' Получим класс, который будет создавать формы. Параметр extra=2 означает,
    что на странице с несколькими формами изначально будет появляться 2 формы
    создания авторов.
    '''
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    ''' Обработчик будет обрабатывать GET- и POST-запросы. POST-запрос будет
    содержать в себе уже заполненные данные формы.
    '''
    if request.method == 'POST':
        ''' Формсет заполняется данными, пришедшими в запросе. prefix="*" - это
        можно иметь на странице не только несколько форм, но и несколько
        формсетов, а параметр позволяет их отличать при запросе.
        '''
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        if author_formset.is_valid():   # Проверка валидности формы
            for author_form in author_formset:
                author_form.save()      # Сохранение каждой формы в формсете
            return HttpResponseRedirect(reverse_lazy('authors_list'))
    else:   # Если получен GET-запрос, в ответ просто отрисовка форм
        # Формсет инициализируется и ниже передаётся в контекст шаблона
        author_formset = AuthorFormSet(prefix='authors')
    return render(request, 'manage_authors.html', {'author_formset': author_formset})

def books_authors_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if author_formset.is_valid() and book_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            for book_form in book_formset:
                book_form.save()
            return HttpResponseRedirect(reverse_lazy('authors_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render(request, 'manage_books_authors.html', {'author_formset': author_formset, 'book_formset': book_formset})

def publishers_list(request):
    template = loader.get_template('publishers.html')
    publishers = Publisher.objects.all()
    publish_data = {
        'publishers': publishers,
    }
    return HttpResponse(template.render(publish_data, request))

def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')
