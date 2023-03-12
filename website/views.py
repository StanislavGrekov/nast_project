from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def answer(request):

    template_name = 'templ/index.html'
    contex = {'answer': 'Done'}
    print('yes')
    return render(request, template_name, contex)


def httpresponse(request):
    return HttpResponse('TESTIROVANIE')