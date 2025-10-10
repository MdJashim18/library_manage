from django.http import HttpResponse
from django.shortcuts import render, redirect
from library.models import Book, Department
from django.db.models import Q

def home(request):
    department_slug = request.GET.get('department')
    query = request.GET.get('q', '')
    departments = Department.objects.all()
    books = Book.objects.all()
   
    if department_slug:
        books = books.filter(department__slug=department_slug)

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )

    context = {
        'books': books,
        'departments': departments,
        'selected_department': department_slug,
        'query': query
    }

    return render(request, 'base.html', context)
