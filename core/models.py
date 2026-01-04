from django.db import models


class Faculte(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom


class Departement(models.Model):
    faculte = models.ForeignKey(
        Faculte,
        on_delete=models.CASCADE,
        related_name="departements"
    )
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom


class Formation(models.Model):
    departement = models.ForeignKey(
        Departement,
        on_delete=models.CASCADE,
        related_name="formations"
    )
    titre = models.CharField(max_length=150)
    niveau = models.CharField(
        max_length=50,
        choices=[
            ("Licence", "Licence"),
            ("Master", "Master"),
            ("Doctorat", "Doctorat"),
        ]
    )
    duree = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"{self.titre} ({self.niveau})"


class Actualite(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateField(auto_now_add=True)
    # Nouvelle ligne pour l'image (optionnelle)
    image = models.ImageField(upload_to='actualites/', null=True, blank=True)

    def __str__(self):
        return self.titre

class PageUniversite(models.Model):
    titre = models.CharField(max_length=200, default="Université Exemple")
    historique = models.TextField(null=True, blank=True)
    missions = models.TextField(null=True, blank=True)
    valeurs = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.titre
    

class Enseignant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)  # Professeur, Maître de conférence, etc.
    specialite = models.CharField(max_length=200, default="")
    photo = models.ImageField(upload_to='enseignants/', blank=True, null=True)
    departement = models.ForeignKey('Departement', on_delete=models.CASCADE, related_name='enseignants')

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Matiere(models.Model):
    # La formation à laquelle appartient la matière
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name='matieres')
    
    # Nom de la matière
    nom = models.CharField(max_length=100)
    
    # Niveau détaillé : ex. Licence 1, Licence 2, Licence 3, Master 1, Master 2
    NIVEAUX_DETAIL = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
        ('D', 'Doctorat'),
    ]
    niveau_detail = models.CharField(max_length=10, choices=NIVEAUX_DETAIL, default='L1')

    def __str__(self):
        return f"{self.nom} ({self.get_niveau_detail_display()})"
    
#Recherche
class AxeRecherche(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    departements = models.ManyToManyField(
        'Departement',
        related_name='axes_recherche',
        blank=True
    )
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titre

#Laboratoire
class Laboratoire(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    departements = models.ManyToManyField(
        'Departement',
        related_name='laboratoires',
        blank=True
    )
    responsables = models.ManyToManyField(
        'Enseignant',
        related_name='laboratoires',
        blank=True
    )
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nom

#Publications scientifiques
class Publication(models.Model):
    titre = models.CharField(max_length=300)
    resume = models.TextField(blank=True)
    date_publication = models.DateField()
    auteurs = models.ManyToManyField('Enseignant', related_name='publications')
    laboratoire = models.ForeignKey(
        'Laboratoire',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='publications'
    )
    axe_recherche = models.ForeignKey(
        'AxeRecherche',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='publications'
    )
    fichier_pdf = models.FileField(upload_to='publications/', blank=True, null=True)
    
    def __str__(self):
        return self.titre
    

class MessageContact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.sujet or 'Sans sujet'}"


# Contenu général des admissions
class Admission(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image = models.ImageField(upload_to='admissions/', blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

# Documents téléchargeables
class DocumentAdmission(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='documents')
    nom = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='admissions/documents/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

# Étapes de la procédure / FAQ
class EtapeAdmission(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='etapes')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    ordre = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return self.titre

