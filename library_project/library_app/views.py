from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

def index(request):
    return render(request, 'library_app/index.html')