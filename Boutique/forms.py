from django import forms
from .models import Client,Produit,Commande,Detail
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
class ClientForm(forms.Form):
   ncli = forms.CharField(label = "Numero Client",max_length = 10)
   nom = forms.CharField(label = "Nom Complet",max_length = 100)
   adresse = forms.CharField(label = "Adresse",max_length = 200)
   localite = forms.CharField(label = "Ville",max_length = 100)
   cat = forms.CharField(label = "Categorie",max_length = 2,required = False)
   compte = forms.DecimalField(label = "Solde Compte",max_digits = 10,decimal_places = 2)
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['npro'].disabled = True
class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['ncom'].disabled = True
class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if 'commande' in self.fields:
                self.fields['commande'].disabled = True
            if 'produit' in self.fields:
                self.fields['produit'].disabled = True

   
class ClientForm1(forms.ModelForm):
   class Meta:
      model = Client
      fields = '__all__'
######
class RegisterForm(UserCreationForm):
   email = forms.EmailField(label='Adresse Email',required=True)
   class Meta:
      model = User
      fields = ['username','email','password1','password2']
