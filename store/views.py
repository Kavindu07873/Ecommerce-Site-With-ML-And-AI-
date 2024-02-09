from django.shortcuts import render ,get_object_or_404 ,redirect
from .models import Product ,ReviewRating
from .models import Category
from orders.models import OrderProduct
from .forms import ReviewForm
from django.contrib import messages ,auth
from carts.models import CartItem
from carts.views import _cart_id
from django.http import HttpResponse 
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from .helperMl import preprocessing, vectorizer, get_prediction
# Create your views here.

def store(request,category_slug=None):
    categories = None
    products =None

    if category_slug != None:
        categories = get_object_or_404(Category ,slug = category_slug)
        products   =Product.objects.all().filter(category = categories , is_available=True)
        paginator = Paginator(products , 3)
        page = request.GET.get('page')
        page_product = paginator.get_page(page)
        product_count = products.count()
    else:
        products =Product.objects.all().filter(is_available =True).order_by('id')
        paginator = Paginator(products , 3)
        page = request.GET.get('page')
        page_product = paginator.get_page(page)
        product_count = products.count()
    
    context = {

        'products':page_product,
        'product_count':product_count
    }
    return render(request , 'store/store.html' , context)

# def product_by_category(request ,category_slug ):
#     categories =None
#     products =None
#     categories = get_object_or_404(Category,slug = category_slug )
#     products = Product.objects.all().filter(Category =categories ,is_available = True)
#     product_count = products.count()
#     context = {
#         'products':products,
#         'product_count':product_count
#     }
#     return render(request , 'store/store.html' , context)


def product_details(request ,category_slug,product_slug ):
    try:
        # category__slug mehema __ dekak dala apita puluwan vena app ekaka thiyenma model ekaka atribute ekak access karanna
        single_product = Product.objects.get(category__slug = category_slug , slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request) , product = single_product).exists()
    except Exception as e:
        raise e
    
# methanin user order ekak gaththgothada nadda kiyala balanawa true , false da kiyala  
# methana error ekak enawa
# Field 'id' expected a number but got <SimpleLazyObject: <django.contrib.auth.models.AnonymousUser object at 0x00000296EE37A8D0>>.
# ekanisa methanata if ekak danawa
    if request.user.is_authenticated:
        try:
            orderproduct =OrderProduct.objects.filter(user = request.user , product_id = single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct =None
    else:
        orderproduct =None

# Get the review
    reviews = ReviewRating.objects.filter(product_id = single_product.id , status = True)

    positive_reviews_count = ReviewRating.objects.filter(
        product_id=single_product.id,
        reviewType='positive',
        status=True
    ).count()

    negative_reviews_count = ReviewRating.objects.filter(
        product_id=single_product.id,
        reviewType='negative',
        status=True
    ).count()


    context = {
        'single_product':single_product,
        'in_cart' : in_cart,
        'orderproduct':orderproduct,
        'reviews' : reviews,
        'positive_reviews_count':positive_reviews_count,
        'negative_reviews_count':negative_reviews_count
    }

    return render(request , 'store/product_details.html' ,context)




def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            Products = Product.objects.order_by('-created_date').filter(Q(description__icontains = keyword) | Q(product_name__icontains = keyword))
            product_count = Products.count()
        context = {
            'products':Products,
             'product_count':product_count   
        }
    return render(request , 'store/store.html',context )



def submit_review(request , product_id):
    url =request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            # methana __id kiyala dala thiyenne user ge id eka ganna acount eken mkd user acount ekath ekka foreign key nisa
            # product__id ekath foreign key nisa ReviewRating wala
            reviews = ReviewRating.objects.get(user__id = request.user.id , product__id = product_id)
            form = ReviewForm(request.POST , instance = reviews)
            if form.is_valid():
                review = form.cleaned_data['review']
                # Your other code here
                # print("prediction", review)
                preprocessed_txt = preprocessing(review)
                vectorized_txt = vectorizer(preprocessed_txt)
                prediction = get_prediction(vectorized_txt)
                # print("prediction",prediction)
                form.instance.reviewType = prediction
                form.save()
                messages.success(request , 'Thank You! You review has been updated.')
            else:
            # Handle form validation errors, e.g., return an error response or render the form again with validation errors
                print("Form is not valid")
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                # Your other code here
                # print("prediction", review)
                preprocessed_txt = preprocessing(data.review)
                vectorized_txt = vectorizer(preprocessed_txt)
                prediction = get_prediction(vectorized_txt)
                # print("prediction",prediction)
                data.reviewType = prediction
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                print("Hello World")
                messages.success(request , 'Thank You! You review has been submited.')
                return redirect(url)
            
