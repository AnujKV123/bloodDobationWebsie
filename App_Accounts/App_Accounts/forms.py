from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from App_Accounts.models import Profile
USER_TYPE = (
    ('select', 'select'),
    ('blood doner', 'Blood Doner'),
)


class SignUpForm(UserCreationForm):
    phone=forms.CharField(label="Mobile No")
    type=forms.CharField(label="User Type",widget=forms.Select(choices=USER_TYPE))
    class Meta:
        model = User
        fields = ('username', 'email', 'type', 'password1', 'password2','phone')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileUpdateForm(forms.ModelForm):
    dob = forms.DateField(label="Date of Birth",widget=forms.TextInput(attrs={'type': 'date'}))
    aboutyou=forms.CharField(label="About You", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'comm',
        'rows': 3,
        'cols': 40,
        'padding': '10px',
    }))
    class Meta:
        model=Profile
        fields=['type','phone','image','city','address','facebook','twitter','instragam','linkedin','gender','bloodgroup',
                'religion','dob','aboutyou'
                ]
