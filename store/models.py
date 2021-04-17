from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

Commande_CHOICES = (
    ('N','Nouveau'),
    ('E','En attente'),
    ('V','Verifié')
)

def is_number(value):
    if value.isdigit() == False:
        raise ValidationError(
            ("%(value)s n'est pas un nombre de telephone vailde"),
            params={'value': value},
        )

class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="clients",null=True,blank=True)
    telephone= models.CharField(max_length=8, null=True,validators=[is_number])
    infos_liv= models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.user.first_name


class Produit(models.Model):
    nom= models.CharField(max_length=50, null=True)
    ref = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=300, null=True)
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE,limit_choices_to={'parent__isnull': False},related_name="produits", null=True)
    marque = models.CharField(max_length=30, null=True)
    tva=models.DecimalField( max_digits=3, decimal_places=1)
    promotion = models.BooleanField(default=False)
    prix = models.DecimalField( max_digits=5, decimal_places=2)
    prix_promo = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    commentaire = models.CharField(max_length=400, null=True,blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

   

    def __str__(self):
     return self.nom

    @property
    def imageURL(self):
             try:
                    url= self.image.url
             except:
                    url= ''
             return url

class Categorie(models.Model):
        name = models.CharField(max_length=100)
        description = models.TextField()
        parent = models.ForeignKey('self', limit_choices_to={'parent__isnull': True},related_name="parente", on_delete=models.CASCADE,blank=True, null=True,)

        def __str__(self):
            return self.name

        def get_cat_par(self):
            return  str(self.parent_set.all().count())

class Commande(models.Model):
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True ,related_name="commandes",)
    date_creation = models.DateTimeField(auto_now_add=True)
    etat = models.CharField(choices=Commande_CHOICES, default="N",max_length=1)
    modification=models.BooleanField(default=False)
    date_modi=models.DateTimeField(auto_now_add=False,null=True,blank=True)
    infos_liv = models.CharField(max_length=400, null=True,blank=True)
    totalHT= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    totaltTTC= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    



    def __str__(self):
        return str(self.id)


class LigneCmd(models.Model):
        produit = models.ForeignKey(Produit, on_delete=models.SET_NULL,related_name="lignecmds", null=True, blank=True)
        commande = models.ForeignKey(Commande, on_delete=models.CASCADE,related_name="lignecmds",null=True, blank=True)
        qte = models.IntegerField(default=0, null=True,validators=[MinValueValidator(0)])
        date_added = models.DateTimeField(auto_now_add=True)

        @property
        def get_total(self):
            return self.qte * self.produit.prix

class Contact(models.Model):
    message= models.CharField(max_length=4000,null=True,blank=True)
    recepteur=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name="recep")
    emetteur=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name="emett")
    sujet=models.CharField(max_length=40,null=True,blank=True)

    def __str__(self):
        return(self.sujet)

    
class ContactVisiteur(models.Model):
    base=models.OneToOneField(Contact, on_delete=models.CASCADE)
    email=models.EmailField()
    nom=models.CharField(max_length=30,null=True,blank=True)
    prenom=models.CharField(max_length=30,null=True,blank=True)
    tel=models.CharField(max_length=8,null=True,blank=True)

    def __str__(self):
        return(self.nom)
