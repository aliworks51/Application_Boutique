from django.contrib import admin
from .models import Client,Produit,Commande,Detail
class DetailInline(admin.TabularInline):
   model = Detail
   extra = 1
class CommandeAdmin(admin.ModelAdmin):
   list_display = ('ncom','client','datecom')
   inlines = [DetailInline]
admin.site.register(Client)
admin.site.register(Produit)
admin.site.register(Detail)
admin.site.register(Commande,CommandeAdmin)

