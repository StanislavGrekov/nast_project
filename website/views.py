# from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

def answer(request):
    template_name = 'templ/index.html'
    contex = {'answer': 'Done'}
    return render(request, template_name, contex)


@api_view(['GET'])
def sample_view(request):
    return Response({'message': 'Hello world!'})
