from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,"SUB/dashboard.html")
def about(request):
    return HttpResponse("A propos de nous")

#exercice partie 1:
# 1 page Catalogue 
def catalogue(request):
     return render(request, "SUB/catalogue.html")
    # 3:
     context = {
        "magasin": "Bot7anot"
     }

     return render(request, "SUB/catalogue.html", context)
