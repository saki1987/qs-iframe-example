from django import forms
 
class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()

class UserForm(forms.Form):
	username = forms.CharField(label='username',max_length=128)
	password = forms.CharField(label='password',widget=forms.PasswordInput())
	email	 = forms.EmailField(label='email',required=False)
	phone	 = forms.CharField(label='phone',max_length=11,required=False)

