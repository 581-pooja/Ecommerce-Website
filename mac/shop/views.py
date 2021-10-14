from django.shortcuts import render , redirect , HttpResponseRedirect
from django.http import HttpResponse
from .models import Product, Contact , Orders , OrderUpdate , Register
from django.contrib import messages
from math import ceil
from django.views.decorators.csrf import csrf_exempt
# from PayTm import Checksum
import datetime
import json
from passlib.hash import sha256_crypt
from django.contrib.auth.hashers import make_password ,check_password
from django.contrib import messages
from shop.middlewares.auth import auth_middleware

MERCHANT_KEY = 'WorldP64425807474247'


# HTML Pages
def index(request):
    # username = request.session['username']
    # print(username)
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}

    # For checking sessions created or not
    print(request.session.get('username'))
    print(request.session.get('customer_id'))
    print(request.session.get('email'))
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        msg_date= datetime.datetime.now()
        print(name)
        # contact = Contact(name=name, email=email, phone=phone, desc=desc, msg_date= msg_date)
        # contact.save()
        # messages.success(request, 'Your messsage have been sended.Our Team will contact you Soon')
    return render(request, 'shop/contact.html')


def tracker(request):
    # if request.method == "POST":
    #     orderId = request.POST.get('orderId', '')
    #     email = request.POST.get('email','')
    #     print(orderId, email)
    #     try:
    #         order = Orders.objects.filter(order_id = orderId, email= email)
    #         if len(order)>0:
    #             update = OrderUpdate.objects.filter(order_Id = orderId)
    #             updates = []
    #             for item in update:
    #                 updates.append({'text':item.update_desc, 'time': item.timestamp})
    #                 response = json.dumps(updates, default=str)
    #             return HttpResponse(response)
    #         else:
    #             return HttpResponse('{}')
    #     except Exception as e:
    #         return HttpResponse('{}')
    return render(request, 'shop/tracker.html')


def trackerResponse(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email','')
        print(orderId, email)
        try:
            order = Orders.objects.filter(order_id = orderId, email= email)
            print(order)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id = orderId)
                print(update)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
        return render(request, 'shop/trackerResponse.html', response)   
    return render(request, 'shop/trackerResponse.html')

# Search function
def searchMatch(query, item):
    ''' return true only if uery matchs the item '''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search').lower()
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        if len(prod) != 0:
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'shop/search.html', params)
    # return HttpResponse("Seach Page")


def productView(request , myid):
    # Fetch the products using id giving name myid
    # since django create primary key by itself ie. id
    product = Product.objects.filter(id = myid)
    print(product)
    print(myid)
    # product passed for productView Page we wish to access : product here views.py name
    params = {'product':product[0], 'product_id':myid}
    return render(request, 'shop/prodView.html', params)


def checkoutOrders(request):
    return render(request, 'shop/checkoutOrders.html')

@auth_middleware
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', 0)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        order = Orders(items_json = items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        thank = True
        update = OrderUpdate(order_id = order.order_id, update_desc = "The order has been Placed")
        update.save()
        id = order.order_id
        # return render(request, 'shop/success.html', {'thank': thank , 'id' : id})
        # Request paytm to transfer the amount to your account after payment by user

        param_dict={

            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        
        # paytmChecksum = Checksum.generateSignature(param_dict, MERCHANT_KEY)

        return  render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')


def success(request):
    # May be this code is redundant
    return render(request, 'shop/success.html')
    # return HttpResponse("Search of Shop Page!!")

# Authentication API's
def register(request):
    '''for perdefined emails are not allowed to added to databases'''
    if request.method == "POST":
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        isCustomerExists = Register.isExists(email)
        print(isCustomerExists)
        if not isCustomerExists:
            if password == confirm_password:
                hash_password = make_password(password)
                register = Register(username=username, email=email, password=hash_password)
                register.save()
                messages.success(request, f'{username} you have successfully registered.Happy Shopping!')
                return redirect('/shop/')
            else:
                print("Password not matched")
                messages.success(request, f'{username} check password!')
                return render(request, 'shop/register.html') # right now return register page
        else:
            messages.info(request, f'This email already exists in our Database! so you can Login.')
            return render(request, 'shop/register.html')
    return render(request, 'shop/register.html')


def login(request):
    '''This is working for both success email and unsuccessful emails Todo: Add lower case allowed to emails'''
    if request.method == "GET":
        login.returnUrl = request.GET.get('return_url')
        return render(request, 'shop/login.html')

    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        customer = Register.get_customer_by_email(email)
        # print(email, password)
        # error_message = None
        # print(customer)
        if customer:
            # Customer Exists
            flag = check_password(password, customer.password)
            # print(flag)
            if flag:
                # session created and storing email, name , customer_id in the session
                request.session['customer_id'] = customer.register_id
                request.session['username'] = customer.username
                request.session['email'] = customer.email
                username = customer.username
                if login.returnUrl:
                    return HttpResponseRedirect(login.returnUrl)
                else:
                    messages.success(request, f'{username} you have successfully Logged In.Happy Shopping!')
                    login.returnUrl = None
                    return redirect('/shop/')
            else:
                # Customer Exists but made password incorrect
                messages.warning(request, f'Invalid Password!')
                return render(request, 'shop/login.html')
        else:
            messages.warning(request, f'Invalid Email!')
            return render(request, 'shop/login.html')
    return render(request, 'shop/login.html')


def logout(request):
    request.session.clear()
    return redirect('/shop/')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    # since it will post request so we have to remove csrf
    # csrf_exempt is decorator which changes the function functionality for sometime
    return HttpResponse("Done")