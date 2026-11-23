from django import forms

class EventRegistrationForm(forms.Form):
    name = forms.CharField(
        label='Повне ім\'я',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Електронна пошта',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    ticket_type = forms.ChoiceField(
        label='Тип квитка',
        choices=[
            ('standard', 'Стандартний'),
            ('vip', 'VIP'),
            ('student', 'Студентський'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='Повідомлення організаторам',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.split()) < 2:
            raise forms.ValidationError('Будь ласка, введіть ім\'я та прізвище.')
        return name
