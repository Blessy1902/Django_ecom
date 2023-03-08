from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm




class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class AddProductForm(forms.ModelForm):
    image = forms.ImageField(required=True, label='Product Image')
    class Meta:
        model = Product
        fields = ('name','category', 'price', 'image', 'user')

		
class ProductForm(ModelForm):

    class Meta :
        model = Product
        fields= "__all__"

class CheckoutForm(forms.Form):
    billing_address = forms.CharField(required=True)
    
    card_number = forms.IntegerField(required=True)
    card_expiry = forms.DateField(required=True)
    card_cvv = forms.IntegerField(required=True)   