from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from p_library.models import Author, Book, Publisher
from p_library.forms import AuthorForm

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
