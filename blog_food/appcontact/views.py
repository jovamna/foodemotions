from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from blog_food.settings import EMAIL_HOST_USER
from .forms import ContactForm
from apprecetas.models import Kategory
from apprecetasalzum.models import Category

#from django.http import JsonResponse
#import re
#from .models import SubscribedUsers
#from django.core.mail import send_mail
from django.conf import settings

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
            email = EmailMessage(
                "FoodingEmotion: Nuevo mensaje de contacto",
                "De {} <{}>\n\nEscribió:\n\n{}".format(name, email, content),
                #"emotionsfood@gmail.com",
                EMAIL_HOST_USER,
                ["emotionsfood@gmail.com"],
                reply_to=[email])
            # Lo enviamos y redireccionamos
            try:
                email.send()
                # Todo ha ido bien, redireccionamos a OK
                return redirect(reverse('appcontact:contacto') + "?ok")
            except:
                # Algo no ha ido bien, redireccionamos a FAIL
                return redirect(reverse('appcontact:contacto') + "?fail")

    context = {
        'form': contact_form,
        'kategory': kategory,
        'kategories': kategories,
        'categories': categories,
    }

    print(contact_form)

    return render(request, "appcontact/contacto.html", context)


#def suscribe(request):
#if request.method == 'POST':
#post_data = request.POST.copy()
#email = post_data.get("email", None)
#name = post_data.get("name", None)
#subscribedUsers = SubscribedUsers()
#subscribedUsers.email = email
#subscribedUsers.name = name
#subscribedUsers.save()
# send a confirmation mail
#subject = 'NewsLetter Subscription'
#message = 'Hello ' + name + ', Thanks for subscribing us. You will get notification of latest articles posted on our website. Please do not reply on this email.'
#email_from = settings.EMAIL_HOST_USER
#recipient_list = [
#email,
#]
#send_mail(subject, message, email_from, recipient_list)
#res = JsonResponse({'msg': 'Thanks. Subscribed Successfully!'})
#return res
#return render(request, 'suscribirse.html')

#def validate_email(request):
#email = request.POST.get("email", None)
#if email is None:
#res = JsonResponse({'msg': 'Email is required.'})
#elif SubscribedUsers.objects.get(email=email):
#res = JsonResponse({'msg': 'Email Address already exists'})
#elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",
#email):
#res = JsonResponse({'msg': 'Invalid Email Address'})
#else:
#res = JsonResponse({'msg': ''})
#return res
