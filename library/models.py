from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=50, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='library/',blank=True, null=True)

    def __str__(self):
        return f"{self.title} — {self.author}"
    


class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('return_pending', 'Return Pending'),
        ('returned', 'Returned'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def approve(self):
        self.status = 'approved'
        self.due_date = timezone.now() + timedelta(days=7)
        self.book.available_copies -= 1
        self.book.save()
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()

    def mark_returned(self):
        self.status = 'returned'
        self.return_date = timezone.now()
        self.book.available_copies += 1  # ✅ copy increase
        self.book.save()
        self.save()


    def __str__(self):
        return f"{self.student.username} - {self.book.title} ({self.status})"