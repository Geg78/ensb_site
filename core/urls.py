from django import views
from django.urls import path
from .views import accueil, admissions, contact, laboratoire_detail, laboratoires_list, publication_detail, publications_list, recherche_home, axes_recherche_list, axe_recherche_detail, departement_detail, departements_par_faculte, accueil_formation, formations_par_departement,liste_actualites, detail_actualite, universite, faculte_departements

urlpatterns = [
    path('', accueil, name='accueil'),
    path('faculte/<int:faculte_id>/', departements_par_faculte, name='departements'),
    path('departement/<int:departement_id>/', formations_par_departement, name='formations'),
    path('actualites/', liste_actualites, name='actualites'),
    path('actualites/<int:actualite_id>/', detail_actualite, name='detail_actualite'),
    path('universite/', universite, name='universite'),
    path('formations/',accueil_formation,name='fac_dep_form'),
    path('detail_departement/<int:departement_id>/', departement_detail, name='departement_detail'),
    path('recherche/', recherche_home, name='recherche_home'),
    path('recherche/axes_recherche/', axes_recherche_list, name='axes_recherche'),
    path('recherche/axes/<int:axe_id>/', axe_recherche_detail, name='axe_recherche_detail'),
    path('recherche/laboratoires/', laboratoires_list, name='laboratoires_list'),
    path('recherche/laboratoires/<int:labo_id>/', laboratoire_detail, name='laboratoire_detail'),
    path('recherche/publications/', publications_list, name='publications_list'),
    path('recherche/publications/<int:pub_id>/', publication_detail, name='publication_detail'),
    path('contact/', contact, name='contact'),
    path('admissions/', admissions, name='admissions'),
]
