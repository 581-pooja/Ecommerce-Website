from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from math import ceil

# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)
    allProds = []
    catprods = Product.objects.values('category', 'id')
    # print("Catprods: " , catprods)

    cats = {item['category'] for item in catprods}
    # print("cats: " , catprods)

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        # print(prod)
        n = len(prod)
        # print(n)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
        # print(allProds)
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')
    
def contact(request):
    return render(request, 'shop/contact.html')

def tracker(request):
    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')
    # return HttpResponse("Search of Shop Page!!")

def productView(request , myid):
    # Fetch the products using id giving name myid
    # since django create primary key by itself ie. id
    product = Product.objects.filter(id = myid)
    print(product)
    # product passed for productView Page we wish to access : product here views.py name
    params = {'product':product[0]}
    return render(request, 'shop/prodView.html', params)

def checkout(request):
    return render(request, 'shop/checkout.html')
