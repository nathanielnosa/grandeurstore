from django import forms
from . models import Profile

class UserProfile(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # username=  forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})),
    # email=  forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'})),

    class Meta:
        model = Profile
        fields = ['fullname','username','email','password1','password2','phone','gender','profile_pix']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'email': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'phone':forms.TextInput(attrs={'class': 'form-control my-2'}),
            'gender':forms.Select(attrs={'class': 'form-control my-2'}),
            'profile_pix':forms.FileInput(attrs={'class': 'form-control my-2'}),
        }

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname','username','email','phone','gender','profile_pix']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'email': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'phone':forms.TextInput(attrs={'class': 'form-control my-2'}),
            'gender':forms.Select(attrs={'class': 'form-control my-2'}),
            'profile_pix':forms.FileInput(attrs={'class': 'form-control my-2'}),
        }