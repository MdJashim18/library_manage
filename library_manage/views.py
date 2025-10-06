from django.http import HttpResponse
from django.shortcuts import render, redirect
from library.models import Book, Department

def home(request):
    department_slug = request.GET.get('department')
    departments = Department.objects.all()

    if department_slug:
        books = Book.objects.filter(department__slug=department_slug)
    else:
        books = Book.objects.all()

    return render(request, 'base.html', {
        'books': books,
        'departments': departments,
        'selected_department': department_slug,
    })