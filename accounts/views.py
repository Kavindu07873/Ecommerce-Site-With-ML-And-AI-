from multiprocessing import AuthenticationError
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages ,auth
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

# verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from orders.models import Order

from carts.views import _cart_id
from carts.models import Cart ,CartItem
import requests

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            # user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,phone_number=phone_number, username=username, password=password)
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=username, password=password)
            user.phone_number = phone_number
            # harinm methana is active danna ba activatin method eke thamai danna ona
            #  m ahe wada nathi nisaa essarahata karagena yanna on anisa mehema kare

            user.is_active = True
            print(user)
            user.save()

            # User Activation  
            # verification email
            # current_site = get_current_site(request)
            # mail_subject = 'Please activate your account'
            # message = render_to_string('accounts/account_verification_email.html', {
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            
            # print(email)
            
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # print(send_email)
            # send_email.send()

            
            messages.success(request, 'Registation sucessful.')
            return redirect('login') 

        else:
            print("not save")
    else:
        print("why wada naththe")
        form = RegistrationForm()
        

    context = {
         'form':form,
    }
    return render(request , 'accounts/register.html' , context)

def login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email = email ,password=password)

        if user is not None:
            
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart = cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))                   

                    # Get the cart item from the user to access his product variations 
                    cart_item = CartItem.objects.filter(user = user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        # api list ekak widiyata ganna ona
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)


                    # product_veriation = [1,2,3,4,5,6]
                    # ex_var_list = [4,6,3,5]

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id = item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart = cart)
                            for item in cart_item:
                                item.user =user
                                item.save()

                    # for item in cart_item:
                    #     item.user = user
                    #     item.save()
            except:
                pass    


            auth.login(request , user)
            messages.success(request , 'You Are now logged in..')

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                
                params = dict(x.split('=') for x in query.split('&'))
                print(params)

                if 'next' in params:
                    nextpage = params['next']
                    return redirect(nextpage)
            except:
                return redirect('dashboard')

            
        else:
            print("wada na ")
            messages.error(request , 'Invalid login credentials')
            return redirect('login')
        
    return render(request , 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def activate(request ,uidb64 ,token):
    return HttpResponse("ok")

@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id ,is_ordered = True)
    orders_count = orders.count()
    context = {
        'orders_count' : orders_count,
    }
    return render(request ,'accounts/dashboard.html' ,context)

def forgetpassword(request):
    return render(request , 'accounts/forgetpassword.html')

def my_orders(request):
    orders = Order.objects.filter(user = request.user , is_ordered = True ).order_by('-created_at')
    print(orders)
    context ={
        'orders':orders
    }
    return render(request , 'accounts/my_orders.html' , context)


def edit_profile(request):
    return render(request , 'accounts/edit_profile.html')
