from django.shortcuts import render, get_object_or_404, redirect
from .models import Admission, Faculte, Departement, Laboratoire, Formation, Actualite, PageUniversite, Enseignant, AxeRecherche, Publication
from core import models
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import MessageContact


def accueil(request):
    facultes = Faculte.objects.all()
    actualites = Actualite.objects.order_by('-date_publication')[:3]

    return render(request, 'core/accueil.html', {
        'facultes': facultes,
        'actualites': actualites
    })

def accueil_formation(request):
    facultes = Faculte.objects.all()

    return render(request, 'core/fac_departements.html', {
        'facultes': facultes,
    })


def departements_par_faculte(request, faculte_id):
    faculte = get_object_or_404(Faculte, id=faculte_id)
    departements = faculte.departements.all()
    return render(request, 'core/departements.html', {
        'faculte': faculte,
        'departements': departements
    })


def formations_par_departement(request, departement_id):
    departement = get_object_or_404(Departement, id=departement_id)
    formations = departement.formations.all()
    return render(request, 'core/formations.html', {
        'departement': departement,
        'formations': formations
    })

def liste_actualites(request):
    actualites = Actualite.objects.order_by('-date_publication')
    return render(request, 'core/actualites.html', {
        'actualites': actualites
    })

def detail_actualite(request, actualite_id):
    actualite = get_object_or_404(Actualite, id=actualite_id)
    return render(request, 'core/detail_actualite.html', {
        'actualite': actualite
    })


def universite(request):
    page = PageUniversite.objects.first()  # Prend la première entrée
    return render(request, 'core/universite.html', {'page': page})


def departement_detail(request, departement_id):
    departement = get_object_or_404(Departement, id=departement_id)

    # Préparer les formations par niveau (Licence, Master, Doctorat)
    niveaux = ['Licence', 'Master', 'Doctorat']
    formations_par_niveau = {}
    for niveau in niveaux:
        formations = departement.formations.filter(niveau=niveau).prefetch_related('matieres')
        formations_par_niveau[niveau] = formations

    # Liste des enseignants
    enseignants = departement.enseignants.all()

    return render(request, 'core/departement_detail.html', {
        'departement': departement,
        'formations_par_niveau': formations_par_niveau,
        'enseignants': enseignants,
    })

def faculte_departements(request, faculte_id):
    faculte = get_object_or_404(Faculte, id=faculte_id)
    departements = faculte.departements.all()

    return render(request, 'core/faculte_departements.html', {
        'faculte': faculte,
        'departements': departements
    })

#Recherche
def recherche_home(request):
    return render(request, 'core/recherche/index.html')

def axes_recherche_list(request):
    axes = AxeRecherche.objects.all()
    return render(request, 'core/recherche/axes_list.html', {
        'axes': axes
    })

def axe_recherche_detail(request, axe_id):
    axe = get_object_or_404(AxeRecherche, id=axe_id)
    return render(request, 'core/recherche/axe_detail.html', {
        'axe': axe
    })

#laboratoire views
# Liste de tous les laboratoires
def laboratoires_list(request):
    laboratoires = Laboratoire.objects.all()
    return render(request, 'core/recherche/laboratoires_list.html', {
        'laboratoires': laboratoires
    })

# Détail d’un laboratoire
def laboratoire_detail(request, labo_id):
    labo = get_object_or_404(Laboratoire, id=labo_id)
    return render(request, 'core/recherche/laboratoire_detail.html', {
        'laboratoire': labo
    })


#Les publications scientifiques

# Liste des publications
def publications_list(request):
    query = request.GET.get('q', '')  # récupération du paramètre de recherche
    publications = Publication.objects.all().order_by('-date_publication')

    if query:
        publications = publications.filter(
            models.Q(titre__icontains=query) |
            models.Q(auteurs__nom__icontains=query) |
            models.Q(auteurs__prenom__icontains=query)
        ).distinct()

    return render(request, 'core/recherche/publications_list.html', {
        'publications': publications,
        'query': query
    })


# Détail d’une publication
def publication_detail(request, pub_id):
    publication = get_object_or_404(Publication, id=pub_id)
    return render(request, 'core/recherche/publication_detail.html', {
        'publication': publication
    })

#contact
def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        if not nom or not email or not message:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return redirect('contact')

        contenu_message = f"""
Message envoyé depuis le site ENS

Nom : {nom}
Email : {email}
Sujet : {sujet}

Message :
{message}
        """

        # 1️⃣ Sauvegarder en base
        MessageContact.objects.create(
            nom=nom,
            email=email,
            sujet=sujet,
            message=message
        )

        try:
            # 2️⃣ Email à l'administration
            mail_admin = EmailMessage(
                sujet if sujet else "Message depuis le site ENS",
                contenu_message,
                settings.DEFAULT_FROM_EMAIL,
                ['contact@ens.edu'],
                reply_to=[email],
            )
            mail_admin.send()

            # 3️⃣ Email d'accusé de réception à l'utilisateur
            mail_accuse = EmailMessage(
                "Confirmation de réception de votre message",
                f"Bonjour {nom},\n\nMerci pour votre message. "
                "Nous vous répondrons dans les plus brefs délais.\n\n"
                "Cordialement,\nL'équipe ENS",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            mail_accuse.send()

            messages.success(request, "Votre message a été envoyé et un accusé de réception vous a été envoyé.")

        except Exception as e:
            print("ERREUR EMAIL :", e)
            messages.error(request,
                "Votre message a été enregistré, mais l'envoi de l'email a échoué."
            )

        return redirect('contact')

    return render(request, 'core/contact.html')

    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        if not nom or not email or not message:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return redirect('contact')

        contenu_message = f"""
Message envoyé depuis le site ENS

Nom : {nom}
Email : {email}
Sujet : {sujet}

Message :
{message}
        """

        # 1️⃣ Sauvegarder en base
        MessageContact.objects.create(
            nom=nom,
            email=email,
            sujet=sujet,
            message=message
        )

        try:
            # 2️⃣ Envoyer l’email
            mail = EmailMessage(
                sujet if sujet else "Message depuis le site ENS",
                contenu_message,
                settings.DEFAULT_FROM_EMAIL,
                ['contact@ens.edu'],
                reply_to=[email],
            )
            mail.send()
            messages.success(request, "Votre message a été envoyé et enregistré avec succès.")

        except Exception as e:
            print("ERREUR EMAIL :", e)
            messages.error(request, "Votre message a été enregistré, mais l'envoi email a échoué.")

        return redirect('contact')

    return render(request, 'core/contact.html')


    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        if not nom or not email or not message:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return redirect('contact')

        contenu_message = f"""
Message envoyé depuis le site ENS

Nom : {nom}
Email : {email}
Sujet : {sujet}

Message :
{message}
        """

        try:
            mail = EmailMessage(
                sujet if sujet else "Message depuis le site ENS",
                contenu_message,
                settings.DEFAULT_FROM_EMAIL,
                ['contact@ens.edu'],
                reply_to=[email],
            )
            mail.send()

            messages.success(request, "Votre message a été envoyé avec succès.")

        except Exception as e:
            print("ERREUR EMAIL :", e)
            messages.error(request, "Erreur lors de l'envoi du message.")

        return redirect('contact')

    return render(request, 'core/contact.html')


    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        if not nom or not email or not message:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return redirect('contact')

        contenu_message = f"Message envoyé depuis le site ENS : {nom} \n {email} \n {sujet} \n {message}"

        try:
            email_message = EmailMessage( 
                subject=sujet if sujet else "Message depuis le site ENS",
                body=contenu_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['contact@ens.edu'],
                reply_to=[email],   # ✅ fonctionne ici
            )

            email_message.send(fail_silently=False)

            messages.success(
                request,
                "Votre message a été envoyé avec succès."
            )

        except Exception as e:
            # print("ERREUR EMAIL :", e)
            messages.error(
                request,
                "Une erreur est survenue lors de l'envoi du message."
            )

        return redirect('contact')

    return render(request, 'core/contact.html')

def admissions(request):
    infos = Admission.objects.all().order_by('date_publication')
    return render(request, 'core/admissions.html', {'informations': infos})