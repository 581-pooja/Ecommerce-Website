from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact
from math import ceil
import datetime

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
    if request.method == "POST":
        # print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        msg_date= datetime.datetime.now()
        # print(name,email,phone,desc,msg_date)
        contact = Contact(name=name, email=email, phone=phone, desc=desc, msg_date= msg_date)
        contact.save()
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
