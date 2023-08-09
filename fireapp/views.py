from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from .models import Crackers, carosel, similarCrackers,CartItem,Address,Orders,Delivered
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


from django.shortcuts import render
from django.core.mail import send_mail
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! HOME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def home(request):
    crackers = Crackers.objects.all()
    slide = carosel.objects.all()
    print(crackers)

    if request.user.is_authenticated and not request.session.get('welcome_email_sent', False):
        user = request.user.username
        email = request.user.email
        msg = "Welcome to firecrackers!"
        send_mail("Hi " + user, msg, 'your_email@gmail.com', [email])
        request.session['welcome_email_sent'] = True

    print(crackers)
    if request.user.is_staff:
        yes = "yes"
        return render(request, "home.html", {"crackers": crackers, "yes": yes,"slide": slide})

    return render(request, "home.html", {"crackers": crackers, "slide": slide})
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ORDER PAGE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def crackeradminview(request):
    crackers=Crackers.objects.all()
    return render(request,'crackerstable.html',{"crack":crackers})
def similaradminview(request):
    crackers=similarCrackers.objects.all()
    return render(request,'similartable.html',{"crack":crackers})
def similardel(request,id):
    obj=similarCrackers.objects.get(id=id)
    obj.delete()
    return redirect("similaradminview")
def similaredit(request, id):
    crackers = Crackers.objects.all()
    li = [cracker.name for cracker in crackers]

    crack = similarCrackers.objects.get(id=id)
    obj = similarCrackers.objects.get(id=id)

    if request.method == 'POST':
        # Check if the image is being updated
        if 'image' in request.FILES:
            # Delete the previous image from storage if it exists
            if obj.image and os.path.isfile(obj.image.path):
                os.remove(obj.image.path)
            obj.image = request.FILES['image']

        name = request.POST.get("cracker_type")
        selected_cracker = Crackers.objects.get(name=name)
        similarname = request.POST.get("similar_name")
        actual_price = request.POST.get("actual_price")
        discount_price = request.POST.get("discount_price")
        content = request.POST.get("content")

        obj.name = selected_cracker
        obj.similarname = similarname
        obj.actual_price = actual_price
        obj.discount_price = discount_price
        obj.content = content
        obj.save()
        success = "Successfully added."
        return redirect("similaradminview")

    return render(request, "similaredit.html", {"form": crack, "name": li})


def crackdel(request,id):
    obj=Crackers.objects.get(id=id)
    obj.delete()
    return redirect("uploadcrackers")
def payment(request):
    return render(request,"payment.html")
def auth(request):
    return render(request,"auth.html")
@login_required(login_url="auth")
def order(request):


    user = request.user.email
    orderss = Orders.objects.filter(username=user)
    if Address.objects.filter(User=request.user.email).exists():
        add=Address.objects.get(User=request.user.email)
        for order in orderss:
            delivered_orders = Delivered.objects.filter(data=order)
            order.delivered_dates = [delivered_order.delivery_date for delivered_order in delivered_orders]
            print(order.delivered_dates)
        return render(request, 'order.html', {"order": orderss, "add": add})
    else:
        return HttpResponse("<center><h1>NO PRODUCTS</H1></center>")
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! PRODUCT LIST !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def productselect(request, productselect):
    obj = similarCrackers.objects.filter(name__name=productselect)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(username=request.user.email)
        yes = ''
        if cart_items:
            yes = "yes"
        product_names_in_cart = [item.product_name for item in cart_items]

        for product in obj:
            product.in_cart = True if product.similarname in product_names_in_cart else False

        return render(request, "productlist.html", {"productlist": obj, "in_cart_products": product_names_in_cart, "yes": yes})
    else:
        product_names_in_cart = []
        for product in obj:
            product.in_cart = False

        return render(request, "productlist.html", {"productlist": obj, "in_cart_products": product_names_in_cart, "yes": ''})






# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! SIMILARCRACKERS UPLOAD !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def similarcrackers(request):
    crackers = Crackers.objects.all()
    li = [cracker.name for cracker in crackers]
    if request.method == 'POST':
        name = request.POST.get("cracker_type")
        image = request.FILES.get("image")
        similarname = request.POST.get("similar_name")
        actual_price = request.POST.get("actual_price")
        discount_price = request.POST.get("discount_price")
        content = request.POST.get("content")

        if similarCrackers.objects.filter(similarname=similarname).exists():
            error_message = "Similar cracker with the same name already exists."
            return render(request, "similarcrackers.html", {"error_message": error_message, "obj": li})
        else:
            cracker = Crackers.objects.get(name=name)
            crac = similarCrackers(name=cracker, image=image, similarname=similarname, actual_price=actual_price, discount_price=discount_price, content=content)
            crac.save()
            success = "Successfully added."
            return render(request, "similarcrackersupload.html", {"obj": li, "success": success})

    return render(request, "similarcrackersupload.html", {"obj": li})



def admins(request):
    return render(request,"admin.html")
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! BANNER UPDATE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def bannerupdate(request):
    if request.method == 'POST':
        for key in request.FILES:
            image = request.FILES[key]
            carosel_obj = carosel.objects.get(id=key)
            carosel_obj.slideimage = image
            carosel_obj.save()
        return redirect('bannerupdate')  # Redirect to the same page after updating the images

    obj=carosel.objects.all()
    return render(request,"bannerupdate.html",{"banners":obj})
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! UPLOAD CRACKERS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def uploadcrackers(request):
    obj=Crackers.objects.all()
    if request.method == 'POST':
        name = request.POST.get("crackerName")
        image = request.FILES.get("crackerImage")

        if Crackers.objects.filter(name=name).exists():
            error_message = "Cracker with the same name already exists."
            return render(request, "crakersupload.html", {"error_message": error_message})

        cracker = Crackers(name=name, image=image)
        cracker.save()

    crackers = Crackers.objects.all()
    return render(request, "crakersupload.html", {"cracker": crackers})

def logout_view(request):
    logout(request)
    return redirect('home')

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ADD TO CART !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required(login_url="auth")

def add_to_cart(request):

    if request.method == 'POST':
        for key,value in request.POST.items():
            print("&&&&&&&&&&&&")
            print(value )

            if key.startswith('add_to_cart_'):
                product_id = key.replace('add_to_cart_', '')
                product_name_key = 'product_name_' + product_id
                print("****")
                print(product_name_key)
                product_name = request.POST.get(product_name_key)
                obj=similarCrackers.objects.get(similarname=product_name)

                username = request.POST.get('username')
                # Create a new cart item instance
                cart_item = CartItem(
                    product_id=product_id,
                    product_name=obj.similarname,
                    content=obj.content,
                    product_price=obj.actual_price,
                    product_discount=obj.discount_price,
                    image=obj.image,
                    username=username
                )
                username = request.POST.get('username')
                obj = similarCrackers.objects.get(similarname=product_name)
                redirect_to = obj.name
                cart_item.save()

        return redirect('productselect',productselect=redirect_to)

    return redirect('home')

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! mycart !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required(login_url="auth")

def mycart_view(request):
    user = request.user.email
    id = request.user.id
    print(user)

    context = {}  # Initialize the context variable

    if CartItem.objects.filter(username=user).exists():
        obj = CartItem.objects.filter(username=user)
        add = Address.objects.filter(User=user)
        context['cart_items'] = obj
        context['add'] = add
        add = Address.objects.filter(User=user)
        context['add'] = add
        return render(request, 'my-cart.html', context)
    else:
        error = "NO PRODUCT"
        return HttpResponse("<center><h1>NO PRODUCTS</h1></center>")

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Address !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def address(request):
    user=request.user.email
    if request.method == 'POST':

        name = request.POST.get('name')
        state = request.POST.get('state')
        email = request.POST.get('email')
        whatsapp = request.POST.get('whatsapp')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')
        pincode = request.POST.get('pincode')

        # Create a new Contact object
        contact = Address(
            name=name,
            state=state,
            email=email,
            whatsapp=whatsapp,
            mobile=mobile,
            address=address,
            landmark=landmark,
            pincode=pincode,
            User=user
        )
        contact.save()
        return redirect("mycart")
        # Redirect to a success page or do further processing

    return render(request, 'address.html')


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! confirm order !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def confirm_order(request):
    user = request.user.email

    try:
        address = Address.objects.get(User=user)
    except Address.DoesNotExist:
        return redirect("address")

    if request.method == 'POST':
        cart_items = CartItem.objects.filter(username=user)

        for item in cart_items:
            print(item)
            print("##########")
            product_id = item.id
            quantity = request.POST.get('quantity_' + str(product_id))
            product_name = request.POST.get('product_name_' + str(product_id))
            product_price = request.POST.get('product_price_' + str(product_id))
            product_discount = request.POST.get('product_discount_' + str(product_id))
            total_amount = request.POST.get('total_' + str(product_id))

            # Create a new order in the Orders model
            if product_name and quantity:
                order = Orders(
                    username=user,
                    quantity=quantity,
                    product_name=product_name,
                    product_price=product_price,
                    product_discount=product_discount,
                    image=item.image.url[7:],
                    orderdate=datetime.now(),
                    total=total_amount
                )
                order.save()

                # Delete the cart item
                CartItem.objects.filter(id=product_id).delete()


        add = Address.objects.get(User=user)
        email = add.email
        orderss = Orders.objects.filter(username=user)

        context = {
            'user': user,
            'address': address,
            'order': orderss
        }
        email_content = render_to_string('email_templates/order_conformation.html', context)

        send_mail(
            subject='Order Confirmation',
            message='',
            html_message=email_content,
            from_email='your_email@gmail.com',
            recipient_list=[email]
        )

        return redirect('order')

    return HttpResponse("Method not allowed")


def pendingstatus(request):
    status=Orders.objects.filter(order_status="PENDING")
    print(status)
    return render(request,"pendingorder.html",{"penstatus":status})
def delivered(request):
    delivered_orders = Delivered.objects.filter(data__order_status="DELIVERED")
    print(delivered_orders)
    return render(request, "delivered.html", {"delivered_orders": delivered_orders})


def delivers(request, id,user):
    # Get the Orders object based on the provided id and username or raise a 404 error if not found
    order = Orders.objects.get(id=id, username=user)

    print("YYYYYYYYYYYYYYYYYYYYYI IIIIIIIIIII")

    # Update the order status to "DELIVERED" in the Orders model
    order.order_status = "DELIVERED"

    # Save the changes to the Orders model
    order.save()

    # Create a new instance of the Delivered model and save it with the current date as delivery_date
    ordered_date = datetime.now()
    delivered_order = Delivered(data=order, delivery_date=ordered_date)
    delivered_order.save()

    return redirect("pendingstatus")