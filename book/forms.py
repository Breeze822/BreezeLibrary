# Author :Breeze_xylf
# Date :
from django import forms
from .models import Book,Category,Publisher,Member,Profile,BorrowRecord
# from flatpickr import DatePickerInput

class BookCreateEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('author',
                  'title',
                  'description',
                  'quantity',
                  'category',
                  'publisher',
                  'status',
                  'bookshelf_number',
                  'floor_number')


class PubCreatedEditForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields =('name',
                 'city',
                 'contact',)

class MemberCreateEditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('name',
                  'gender',
                  'age',
                  'email',
                  'city',
                  'phone_number',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic',
                  'bio',
                  'phone_number',
                  'email')

class BorrowRecordCreateForm(forms.ModelForm):
    borrower = forms.CharField(label='Borrower',
                               widget=forms.TextInput(attrs={'placeholder':'Search Member...'}))
    book = forms.CharField(help_text="type book name")

    class Meta:
        model = BorrowRecord
        fields = ['borrower',
                  'book',
                  'quantity',
                  'start_day',
                  'end_day']
        # widgets = {
        #     'start_day': DatePickerInput(options={"dateFormat": "Y-m-d", }),
        #     'end_day': DatePickerInput(options={"dateFormat": "Y-m-d", }),
        # }
        widgets = {'start_day': forms.DateTimeInput(attrs={'class': 'datepicker'}),
                   'end_day': forms.DateTimeInput(attrs={'class': 'datepicker'})}
