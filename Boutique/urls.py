
from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.liste_clients, name='clients'),
    path('client/ajouter/',views.ajouter_client,name='ajouter_client'),
    path('client/<str:id_client>/', views.client_commandes, name='client_commandes'),
    # path('client/modifier/<str:pk>/',views.modifier_client,name='modifier_client'),
    # path('client/supprimer/<str:pk>/',views.supprimer_client,name='supprimer_client'),
 
    path('produits/', views.liste_produits, name='produits'),
    path('produit/ajouter/',views.ajouter_produit,name='ajouter_produit'),
    path('produit/modifier/<str:pk>/',views.modifier_produit,name='modifier_produit'),
    path('produit/supprimer/<str:pk>/',views.supprimer_produit,name='supprimer_produit'),   
   
    path('commandes/', views.liste_commandes, name='commandes'),
    path('commande/ajouter/',views.ajouter_commande,name='ajouter_commande'),
    path('commande/modifier/<str:pk>/',views.modifier_commande,name='modifier_commande'),
    path('commande/supprimer/<str:pk>/',views.supprimer_commande,name='supprimer_commande'),
    
    path('details/', views.liste_details, name='details'),
    path('detail/ajouter/',views.ajouter_detail,name='ajouter_detail'),
    path('detail/modifier/<str:ncom>/<str:npro>/', views.modifier_detail, name='modifier_detail'),
    path('detail/supprimer/<str:ncom>/<str:npro>/', views.supprimer_detail, name='supprimer_detail'),
    
    #version pro 
    path('update/<int:ob>/<str:pk>/<str:pk2>/',views.update,name="update"),
    path('delete/<int:ob>/<str:pk>/<str:pk2>/',views.delete,name="delete"),

#######

    path('register/',views.register,name='register'),
    path('login/',views.connexion,name='connexion'),
    path('logout/',views.deconnexion,name='deconnexion'),

    path('admin-dashboard/',views.tableau_bord_admin,name='admin_dashboard'),
    path('monprofil/',views.monprofil,name='monprofil'),
    path('403/',views.acces_refuse,name='403'),
]


