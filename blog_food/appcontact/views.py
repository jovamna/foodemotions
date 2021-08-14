from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from .forms import ContactForm
from apprecetas.models import Kategory
from apprecetasalzum.models import Category

# Create your views here.


def contact(request):
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES

    categories = Category.objects.filter(
        parent=None)  #SOLO LAS CATEGORIAS RECETAS DIETETICAS

    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            content = request.POST.get('content', '')
            #enviamos el correo y redireccionamos
            email = EmailMessage("La Caffettiera: Nuevo mensaje de contacto",
                                 "De {} <{}>\n\nEscribió:\n\n{}".format(
                                     name, email, content),
                                 "no-contestar@inbox.mailtrap.io",
                                 ["emotionsfood@gmail.com"],
                                 reply_to=[email])
            # Lo enviamos y redireccionamos
            try:
                email.send()
                # Todo ha ido bien, redireccionamos a OK
                return redirect(reverse('contacto') + "?ok")
            except:
                # Algo no ha ido bien, redireccionamos a FAIL
                return redirect(reverse('contacto') + "?fail")

    return render(
        request, "appcontact/contacto.html", {
            'form': contact_form,
            'kategory': kategory,
            'kategories': kategories,
            'categories': categories,
        })
