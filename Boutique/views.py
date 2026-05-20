from django.shortcuts import render, get_object_or_404,redirect
from datetime import date
from .models import Client,Produit,Commande,Detail
from .forms import ClientForm1,ClientForm,ProduitForm,CommandeForm,DetailForm,RegisterForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

@login_required
def liste_clients(request):
    data_clients = Client.objects.all()
    return render(request,'Boutique/clients.html',{'clients':data_clients})
@login_required
def liste_produits(request):
    data_produits = Produit.objects.all()
    return render(request,'Boutique/produits.html',{'produit':data_produits})
@login_required  
def liste_commandes(request):
    data_commandes = Commande.objects.select_related('client').all()
    return render(request,'Boutique/commandes.html',{'commandes':data_commandes})
       
def client_commandes(request, id_client):
    client = get_object_or_404(Client,ncli=id_client)
    commandes = Commande.objects.filter(client=client)

    return render(request, 'Boutique/client_commandes.html', {
        'client': client,
        'commandes': commandes
    })
@login_required     
def liste_details(request):
    data_details = Detail.objects.select_related('commande','produit').all()
    return render(request,'Boutique/details.html',{'details':data_details})
    
def ajouter_client(request):
    if request.method == 'POST':
       form = ClientForm(request.POST)
       if form.is_valid():
          Client.objects.create(**form.cleaned_data)
          return redirect('clients')
    else:
       form = ClientForm()
    return render(request,'Boutique/forms.html',{'form':form,'titre':"Ajouter un Client"})
# @permission_required('Boutique.change_client')
# def modifier_client(request,pk):
#     client = get_object_or_404(Client,ncli=pk)
#     if request.method == "POST":
#        form = ClientForm(request.POST)
#        if form.is_valid():
#           Client.objects.filter(ncli=pk).update(**form.cleaned_data)
#        return redirect('clients')
#     else:
#        form = ClientForm(initial={
#              'ncli':client.ncli,'nom':client.nom,'adresse':client.adresse,'localite':client.localite,
#               'cat':client.cat,'compte':client.compte
#               })
#     return render(request,'Boutique/forms.html',{'form':form,'titre':"Modefier Client"})

# @permission_required('Boutique.delete_client')
# def supprimer_client(request,pk):
#     client = get_object_or_404(Client,ncli=pk)
#     if request.method == "POST":
#        client.delete()
#        return redirect('clients')
#     return render(request,'Boutique/delete_confirm.html',{'objet':client,'type':"le client"})
def ajouter_produit(request):
    if request.method == 'POST':
       form = ProduitForm(request.POST)
       if form.is_valid():
          form.save()
          return redirect('produits')
    else:
       form = ProduitForm()
    return render(request,'Boutique/forms.html',{'form':form,'titre':"Ajouter un produit"})

@permission_required('Boutique.change_produit')
def modifier_produit(request,pk):
    produit = get_object_or_404(Produit,pk=pk)
    if request.method == "POST":
       form = ProduitForm(request.POST,instance=produit)
       if form.is_valid():
          form.save()
       return redirect('produits')
    else:
       form = ProduitForm(instance=produit)
    return render(request,'Boutique/forms.html',{'form':form,'titre':"Modefier Produit"})

@permission_required('Boutique.delete_produit')
def supprimer_produit(request,pk):
    produit = get_object_or_404(Produit,pk=pk)
    if request.method == "POST":
       produit.delete()
       return redirect('produits')
    return render(request,'Boutique/delete_confirm.html',{'objet':produit,'type':"le produit"})   
def ajouter_commande(request):
    if request.method == 'POST':
       form = CommandeForm(request.POST)
       if form.is_valid():
          form.save()
          return redirect('commandes')
    else:
       form = CommandeForm()
    return render(request,'Boutique/forms.html',{'form':form,'titre':"Ajouter un Commande"})

@permission_required('Boutique.change_commande')
def modifier_commande(request,pk):
    commande = get_object_or_404(Commande,ncom=int(pk))
    if request.method == "POST":
       form = CommandeForm(request.POST,instance=commande)
       if form.is_valid():
          form.save()
       return redirect('commandes')
    else:
       form = CommandeForm(instance=commande)
    return render(request,'Boutique/forms.html',{'form':form,'titre':f"Modefier commande n {pk}"})

@permission_required('Boutique.delete_commande')
def supprimer_commande(request,pk):
    commande = get_object_or_404(Commande,ncom=int(pk))
    if request.method == "POST":
       commande.delete()
       return redirect('commandes')
    return render(request,'Boutique/delete_confirm.html',{'objet':commande,'type':"le commande"})
def ajouter_detail(request):
    if request.method == 'POST':
       form = DetailForm(request.POST)
       if form.is_valid():
          form.save()
          return redirect('details')
    else:
       form = DetailForm()
    return render(request,'Boutique/forms.html',{'form':form,'titre':"Ajouter les details"})

@permission_required('Boutique.change_detail')
def modifier_detail(request,ncom,npro):
    detail = get_object_or_404(Detail,commande_id=ncom,produit_id=npro)
    if request.method == "POST":
       form = DetailForm(request.POST,instance=detail)
       if form.is_valid():
          form.save()
       return redirect('details')
    else:
       form = DetailForm(instance=detail)
    return render(request,'Boutique/forms.html',{'form':form,'titre':f"Modefier ligne(Com:{ncom},Prod:{npro})"})

@permission_required('Boutique.delete_detail')
def supprimer_detail(request,ncom,npro):
    detail = get_object_or_404(Detail,commande_id=ncom,produit_id=npro)
    if request.method == "POST":
       detail.delete()
       return redirect('details')
    return render(request,'Boutique/delete_confirm.html',{'objet':detail,'type':"cette ligne de commande"})
  
  
  # version pro

MODEL_NAMES = {
      0:'Client',
      1:'Commande',
      2:'Detail',
      3:'Produit'
}
@login_required
def update(request,ob,pk,pk2):
    model_name = MODEL_NAMES.get(ob)
    permission = f'Boutique.change_{model_name.lower()}'
    if not request.user.has_perm(permission):
        return render(request,'Boutique/403.html')
    config = {
      0:(Client,ClientForm1,'ncli','clients'),
      1:(Commande,CommandeForm,'ncom','commandes'),
      3:(Produit,ProduitForm,'npro','produits'),
    }
    if ob == 2:
       instance = get_object_or_404(Detail,commande_id=int(pk),produit_id=pk2)
       form_class = DetailForm
       redir = 'details'
    else:
       model,form_class,pk_field,redir = config[ob]
       lookup_value = int(pk) if ob == 1 else pk
       instance = get_object_or_404(model,**{pk_field:lookup_value})
    if request.method == "POST":
       form = form_class(request.POST,instance=instance)
       if form.is_valid():
          form.save()
          return redirect(redir)
    else:
       form = form_class(instance=instance)
    return render(request,'Boutique/forms.html',{'form':form,'titre':"Modification PRO"})

@login_required
def delete(request,ob,pk,pk2):
       model_name = MODEL_NAMES.get(ob)
       permission = f'Boutique.delete_{model_name.lower()}'
       if not request.user.has_perm(permission):
           return render(request,'Boutique/403.html')
       if ob == 0:
        obj = get_object_or_404(Client,ncli=pk)
        redir = 'clients'
       elif ob == 1:
            obj = get_object_or_404(Commande,ncom=int(pk))
            redir = 'commandes'
       elif ob == 2:
            obj = get_object_or_404(Detail,commande_id=int(pk),produit_id=pk2)
            redir = 'details'
       else:
            obj = get_object_or_404(Produit,npro=pk)
            redir = 'produits'
       if request.method == "POST":
          obj.delete()
          return redirect(redir)
       return render(request,'Boutique/delete_confirm.html',{'objet':obj,'type':"cete element"})
         
    
################
   
    
def register(request):
   if request.method == 'POST':
      form = RegisterForm(request.POST)
      if form.is_valid():
          user = form.save()
          login(request,user)
          return redirect('clients')
   else:
         form = RegisterForm()
   return render(request,'Boutique/auth/register.html',{'form':form})
def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('clients')
    else:
        form = AuthenticationForm()
    return render(request,'Boutique/auth/login.html',{'form':form})

def deconnexion(request):
    logout(request)
    return redirect('connexion')

    

    ###################################


def est_administrateur(user):
    return user.groups.filter(name='Administrateur').exists() or user.is_superuser

@user_passes_test(est_administrateur,login_url='/boutique/login/')
def tableau_bord_admin(request):
    nb_clients = Client.objects.count()
    nb_produits = Produit.objects.count()
    nb_commandes = Commande.objects.count()
    nb_details = Detail.objects.count()
    return render(request,'Boutique/admin_dashboard.html',{
        'nb_clients' : nb_clients,
        'nb_produits' : nb_produits,
        'nb_commandes' : nb_commandes,
        'nb_details' : nb_details,
    }) 
@login_required
def monprofil(request):
    return render(request,'profil/monprofil.html',{'user':request.user})  
def acces_refuse(request): 
    return render(request,'Boutique/403.html')
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
