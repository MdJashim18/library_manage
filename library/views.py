# views.py
from django.shortcuts import render,get_object_or_404,redirect
from .models import Book, Department,BorrowRequest
from .forms import BorrowRequestForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import Book
from .forms import BookForm
from django.contrib import messages
from .models import BorrowRecord
from datetime import timedelta, date


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})





@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BorrowRequestForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.student = request.user
            borrow.book = book
            borrow.save()
            return redirect('student_dashboard')  
    else:
        form = BorrowRequestForm()

    return render(request, 'borrow_form.html', {'form': form, 'book': book})



@staff_member_required
def manage_borrow_requests(request):
    requests = BorrowRequest.objects.all().order_by('-request_date')
    return render(request, 'librarian_dashboard.html', {'requests': requests})




@login_required
def approve_request(request, id):
    req = get_object_or_404(BorrowRequest, id=id)
    req.status = 'approved'
    req.approve()
    return redirect('librarian_dashboard')


@login_required
def reject_request(request, id):
    req = get_object_or_404(BorrowRequest, id=id)
    req.status = 'rejected'
    req.reject()
    return redirect('librarian_dashboard')


@login_required
def return_request(request, pk):
    borrow = get_object_or_404(BorrowRequest, pk=pk)

    if borrow.student != request.user:
        return redirect('student_dashboard')

   
    borrow.status = 'return_pending'
    borrow.save()

    return redirect('student_dashboard')


@login_required
def confirm_return(request, id):
    borrow = get_object_or_404(BorrowRequest, id=id)

    if borrow.status == 'return_pending':
        borrow.mark_returned()  

    return redirect('librarian_dashboard')



@login_required
def student_dashboard(request):
    borrows = BorrowRequest.objects.filter(student=request.user).order_by('-request_date')
    return render(request, 'student_dashboard.html', {'borrows': borrows})



@login_required
def add_book(request):

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('admin_dashboard')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})








def is_admin_or_librarian(user):
    return user.is_staff or user.role in ['librarian', 'admin']


@login_required
@user_passes_test(is_admin_or_librarian)
def book_list(request):
    books = Book.objects.all().order_by('id')
    return render(request, 'book_list.html', {'books': books})


@login_required
@user_passes_test(is_admin_or_librarian)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('library:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})


@login_required
@user_passes_test(is_admin_or_librarian)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('library:book_list')
    return render(request, 'confirm_delete.html', {'book': book})








@login_required
def weekly_report(request):
    today = date.today()
    last_week = today - timedelta(days=7)

    records = BorrowRecord.objects.filter(borrow_date__range=[last_week, today])

    returned_count = records.filter(is_returned=True).count()
    borrowed_count = records.filter(is_returned=False).count()
    unique_students = records.values('student').distinct().count()

    context = {
        'records': records,
        'returned_count': returned_count,
        'borrowed_count': borrowed_count,
        'unique_students': unique_students,
        'last_week': last_week,
        'today': today,
    }
    return render(request, 'weekly_report.html', context)