from django.shortcuts import render
from django.http import HttpResponse

def index_view(request):
    data = {}
    return render(request, 'index_view.html', data)
