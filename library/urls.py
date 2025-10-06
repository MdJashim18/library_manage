from django.urls import path
from .import views

app_name = 'library'

urlpatterns = [
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('librarian/requests/', views.manage_borrow_requests, name='manage_borrow_requests'),
    path('approve/<int:id>/', views.approve_request, name='approve_request'),
    path('reject/<int:id>/', views.reject_request, name='reject_request'),
    path('return/<int:pk>/', views.return_request, name='return_request'),
    path('confirm_return/<int:id>/', views.confirm_return, name='confirm_return'),
    path('add-book/', views.add_book, name='add_book'),
    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),

]
