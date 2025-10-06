from django.http import HttpResponse
from django.shortcuts import render, redirect
from library.models import Book, Department
from django.db.models import Q

def home(request):
    # 🔹 URL query থেকে মান নেওয়া
    department_slug = request.GET.get('department')
    query = request.GET.get('q', '')

    # 🔹 সব ডিপার্টমেন্ট লোড
    departments = Department.objects.all()

    # 🔹 সব বই লোড
    books = Book.objects.all()

    # 🔹 ডিপার্টমেন্ট ফিল্টার
    if department_slug:
        books = books.filter(department__slug=department_slug)

    # 🔹 সার্চ ফিল্টার (title, author, isbn)
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )

    # 🔹 টেমপ্লেটে পাঠানো context
    context = {
        'books': books,
        'departments': departments,
        'selected_department': department_slug,
        'query': query
    }

    return render(request, 'base.html', context)
