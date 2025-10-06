# accounts/urls.py
from django.urls import path
from .views import (
    register_view, login_view, logout_view,
    student_dashboard, teacher_dashboard, librarian_dashboard,admin_dashboard,profile_view,student_form,add_student,edit_student,add_teacher,teacher_form,edit_teacher,librarian_form,add_librarian,edit_librarian
)
from .import views
# app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', profile_view, name='profile'), 

    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('librarian/dashboard/', librarian_dashboard, name='librarian_dashboard'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),


    #Student
    path('student_form/',student_form,name="student_form"),
    path('add_student/',add_student,name="add_student"),
    path('edit_student/<int:id>/',edit_student,name="edit_student"),
    path('user-search/', views.user_search, name='user_search'),

    #Teacher
    path('teacher_form/',teacher_form,name="teacher_form"),
    path('add_teacher/',add_teacher,name="add_teacher"),
    path('edit_teacher/<int:id>/',edit_teacher,name="edit_teacher"),


    #Librarian
    path('librarian_form/',librarian_form,name="librarian_form"),
    path('add_librarian/',add_librarian,name="add_librarian"),
    path('edit_librarian/<int:id>/',edit_librarian,name="edit_librarian"),





    # Admin view URLs
    path('admin/students/', views.admin_view_students, name='admin_view_students'),
    path('admin/teachers/', views.admin_view_teachers, name='admin_view_teachers'),
    path('admin/librarians/', views.admin_view_librarians, name='admin_view_librarians'),
    path('admin/student/<int:id>/', views.admin_student_detail, name='admin_student_detail'),
    path('admin/teacher/<int:id>/', views.admin_teacher_detail, name='admin_teacher_detail'),
    path('admin/librarian/<int:id>/', views.admin_librarian_detail, name='admin_librarian_detail'),

]

