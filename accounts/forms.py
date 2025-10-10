# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Student,Teacher,Librarian

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        roles = list(CustomUser.ROLE_CHOICES)

        if CustomUser.objects.filter(role='librarian').exists():
            roles = [r for r in roles if r[0] != 'librarian']

        if CustomUser.objects.filter(role='admin').exists():
            roles = [r for r in roles if r[0] != 'admin']

        self.fields['role'].choices = roles


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'id': 'user-search'}),
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'


class LibrarianForm(forms.ModelForm):
    class Meta:
        model = Librarian
        fields = '__all__'