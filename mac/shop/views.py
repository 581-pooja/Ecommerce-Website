from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("Index of Shop Page!!")
    return render(request, 'shop/index.html')

def about(request):
    return render(request, 'shop/about.html')
    # return HttpResponse("About of Shop Page!!")

def contact(request):
    return HttpResponse("Contact of Shop Page!!")

def tracker(request):
    return HttpResponse("Tracker of Shop Page!!")

def search(request):
    return HttpResponse("Search of Shop Page!!")

def productView(request):
    return HttpResponse("Product View of Shop Page!!")

def checkout(request):
    return HttpResponse("Checkout of Shop Page!!")
