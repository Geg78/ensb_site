from django.contrib import admin
from .models import Admission, DocumentAdmission, EtapeAdmission, Faculte, Departement, Formation, Enseignant, Actualite, Laboratoire, Matiere, MessageContact, PageUniversite, AxeRecherche, Publication

admin.site.register(Faculte)
admin.site.register(Departement)
admin.site.register(Formation)
admin.site.register(Enseignant)
admin.site.register(Actualite)
admin.site.register(PageUniversite)
admin.site.register(Matiere)
admin.site.register(AxeRecherche)
admin.site.register(Laboratoire)
admin.site.register(Publication)
#Consulter les messages de contact dans l'admin
@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi')
    list_filter = ('date_envoi',)
    search_fields = ('nom', 'email', 'sujet', 'message')

# Admin pour Admission, DocumentAdmission et EtapeAdmission

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publication')

@admin.register(DocumentAdmission)
class DocumentAdmissionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'admission', 'date_ajout')

@admin.register(EtapeAdmission)
class EtapeAdmissionAdmin(admin.ModelAdmin):
    list_display = ('titre', 'admission', 'ordre')
