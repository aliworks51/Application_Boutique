from django.db import models
class Client(models.Model):
  ncli = models.CharField(max_length=10,primary_key=True)
  nom = models.CharField(max_length=100)
  adresse = models.CharField(max_length=200)
  localite = models.CharField(max_length=100)
  cat = models.CharField(max_length=2,null=True,blank=True)
  compte = models.DecimalField(max_digits=10,decimal_places=2)
  def _str_(self):
      return f"{self.nom}({self.ncli})"    
class Produit(models.Model):
   npro = models.CharField(max_length=10,primary_key=True)
   libelle = models.CharField(max_length=100)
   prix = models.IntegerField(default=0)
   qstock = models.IntegerField()  
   def _str_(self):
       return f"{self.libelle}({self.npro})"     
class Commande(models.Model):
   ncom = models.IntegerField(primary_key=True)
   client = models.ForeignKey(Client,on_delete=models.CASCADE)
   datecom = models.DateField() 
   def _str_(self):
       return f"Commande n {self.ncom}"
   def total_articles(self):
       return sum(item.qcom for item in self.lignes.all())     
class Detail(models.Model):
   commande = models.ForeignKey(Commande,on_delete=models.CASCADE,related_name='lignes')
   produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
   qcom = models.IntegerField()
   def _str_(self):
       return f"{self.commande}-{self.produit}-{self.qcom}"   
   class Meta:
      unique_together=('commande','produit')
