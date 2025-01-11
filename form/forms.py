from django import forms

from .models import Form

class FormCreateForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['name', 'valid_student_ids']
        widgets = {
            'valid_student_ids': forms.TextInput(attrs={
                'placeholder': 'Enter student IDs',
                'class': 'form-control tagify-input',
                'data-tagify': 'true',
            }),
        }
