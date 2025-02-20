from django.shortcuts import render,redirect
from django.http import HttpResponse
from website.models import Clients

# Create your views here.

def answer(request):
    template_name = 'templ/index.html'
    contex = {'answer': 'Done'}
    return render(request, template_name, contex)

def postclient(request):

    phone = request.POST.get("phone", "UNDEFINED")
    name = request.POST.get("name", "UNDEFINED")
    message = request.POST.get("message", "UNDEFINED")

    if name == "" or phone == "" or message == "":
        return HttpResponse("Проверьте поля, возможно Вы пытаетесь передать пустые значения!")

    message_from_database = Clients.objects.all()
    for element in message_from_database:
        if name == element.name and phone == element.phone and message == element.message:
            return HttpResponse("УПС, похоже данное сообщение было создано ранее!")

    Clients.objects.create(name=name,phone=phone,message=message)

    template_name = 'templ/result.html'
    contex = {'name': name}

    return render(request, template_name, contex)
