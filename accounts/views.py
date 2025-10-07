# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .import models,forms
from library.models import BorrowRequest
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']

            # Double-check security at backend level
            if role == 'librarian' and CustomUser.objects.filter(role='librarian').exists():
                form.add_error('role', 'A librarian account already exists.')
                return render(request, 'register.html', {'form': form})

            if role == 'admin' and CustomUser.objects.filter(role='admin').exists():
                form.add_error('role', 'An admin account already exists.')
                return render(request, 'register.html', {'form': form})

            user = form.save()
            login(request, user)
            return redirect_user_dashboard(user)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_user_dashboard(user)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return redirect_user_dashboard(request.user)


# Role অনুযায়ী redirect helper function
def redirect_user_dashboard(user):
    if user.role == 'student':
        return redirect('student_dashboard')
    elif user.role == 'teacher':
        return redirect('teacher_dashboard')
    elif user.role == 'librarian':
        return redirect('librarian_dashboard')
    elif user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('login')


# Dashboards
@login_required
def student_dashboard(request):
    try:
        student = models.Student.objects.get(user=request.user)
    except models.Student.DoesNotExist:
        student = None

    # এখানে CustomUser (request.user) দিয়েই query করো
    borrows = BorrowRequest.objects.filter(student=request.user).order_by('-request_date')

    return render(request, 'student_dashboard.html', {
        'student': student,
        'profile': student,
        'borrows': borrows,
    })



@login_required
def teacher_dashboard(request):
    try:
        teacher = models.Teacher.objects.get(user=request.user)
    except models.Teacher.DoesNotExist:
        teacher = None
    return render(request, 'teacher_dashboard.html', {'teacher': teacher,'profile': teacher })


@login_required
def librarian_dashboard(request):
    librarian = None
    try:
        librarian = models.Librarian.objects.get(user=request.user)
    except models.Librarian.DoesNotExist:
        pass

    borrow_requests = BorrowRequest.objects.filter(status='pending').order_by('-request_date')
    return_requests = BorrowRequest.objects.filter(status='return_pending').order_by('-request_date')

    return render(request, 'librarian_dashboard.html', {
        'librarian': librarian,
        'borrow_requests': borrow_requests,
        'return_requests': return_requests,
    })


@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')



def student_form(request):
    student = models.Student.objects.all()
    return render(request,'student_dashboard.html',{'form' : student})

def add_student(request):
    if request.method == 'POST':
        form = forms.StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect('student_form')
        else:
            print(form.errors)
    else:
        form = forms.StudentForm()
    return render(request, 'addStudent.html', {'form': form})

def edit_student(request,id):
    std = models.Student.objects.get(pk=id)
    form = forms.StudentForm(instance=std)
    if request.method=='POST':
        form = forms.StudentForm(request.POST,instance=std)
        if form.is_valid():
            form.save()
            return redirect('admin_view_students')
    return render(request,'edit_student.html',{'form':form})

def user_search(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.filter(username__icontains=query)[:10]
    results = [{'id': u.id, 'text': u.username} for u in users]
    return JsonResponse({'results': results})




def teacher_form(request):
    teacher = models.Teacher.objects.all()
    return render(request,'teacher_dashboard.html',{'form' : teacher})

def add_teacher(request):
    if request.method == 'POST':
        form = forms.TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect('teacher_form')
        else:
            print(form.errors)
    else:
        form = forms.TeacherForm()
    return render(request, 'addTeacher.html', {'form': form})



def edit_teacher(request,id):
    std = models.Teacher.objects.get(pk=id)
    form = forms.TeacherForm(instance=std)
    if request.method=='POST':
        form = forms.TeacherForm(request.POST,instance=std)
        if form.is_valid():
            form.save()
            return redirect('admin_view_teachers')
    return render(request,'edit_teacher.html',{'form':form})



def librarian_form(request):
    librarian = models.Librarian.objects.all()
    return render(request,'librarian_dashboard.html',{'form' : librarian})


def add_librarian(request):
    if request.method == 'POST':
        form = forms.LibrarianForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect('librarian_form')
        else:
            print(form.errors)
    else:
        form = forms.LibrarianForm()
    return render(request, 'addLibrarian.html', {'form': form})

def edit_librarian(request,id):
    std = models.Librarian.objects.get(pk=id)
    form = forms.LibrarianForm(instance=std)
    if request.method=='POST':
        form = forms.LibrarianForm(request.POST,instance=std)
        if form.is_valid():
            form.save()
            return redirect('librarian_dashboard')
    return render(request,'edit_librarrian.html',{'form':form})







# Decorator to allow only admin users
def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.role == 'admin')(view_func)
    return decorated_view_func


# List all students
@admin_required
def admin_view_students(request):
    students = models.Student.objects.all()
    return render(request, 'admin_students.html', {'students': students})


# List all teachers
@admin_required
def admin_view_teachers(request):
    teachers = models.Teacher.objects.all()
    return render(request, 'admin_teachers.html', {'teachers': teachers})


# List all librarians
@admin_required
def admin_view_librarians(request):
    librarians = models.Librarian.objects.all()
    return render(request, 'admin_librarians.html', {'librarians': librarians})


# Individual student detail / dashboard
@admin_required
def admin_student_detail(request, id):
    student = models.Student.objects.get(pk=id)
    borrows = BorrowRequest.objects.filter(student=student.user).order_by('-request_date')
    return render(request, 'admin_student_detail.html', {'student': student, 'borrows': borrows})


# Individual teacher detail
@admin_required
def admin_teacher_detail(request, id):
    teacher = models.Teacher.objects.get(pk=id)
    return render(request, 'admin_teacher_detail.html', {'teacher': teacher})


# Individual librarian detail
@admin_required
def admin_librarian_detail(request, id):
    librarian = models.Librarian.objects.get(pk=id)
    borrow_requests = BorrowRequest.objects.filter(status='pending').order_by('-request_date')
    return render(request, 'admin_librarian_detail.html', {'librarian': librarian, 'borrow_requests': borrow_requests})