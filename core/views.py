from django.shortcuts import render
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def our_history(request):
    return render(request, 'core/our_history.html')

def contact(request):
    return render(request, 'core/contact.html')
