from django.shortcuts import render, redirect
from .models import Cart, Order, Product
from .form import AddProductForm, CheckoutForm, ProductForm
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView,TemplateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .form import NewUserForm, CheckoutForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    
    pro = Product.objects.all()
    pgn = Paginator(pro,4)
    page_num = request.GET.get("page")
    page_obj = pgn.get_page(page_num)
    return render(request, 'home.html',{"prdct": page_obj}) 

def cart(request):
    return render(request,"cart.html")

def AddItems(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.save()
            # messages.info(request, 'Product added successfully!')
            return redirect('home')  
    else:
        form = AddProductForm()
    return render(request, 'addproduct.html', {'form': form})
# class AddPost(CreateView):
#     model = Post
#     template_name = "addproduct.html"
#     fields ="__all__"
# def product_detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     context = {'product': product}
#     return render(request, 'viewproduct.html', context)

def productview(request, id):
    prds = Product.objects.get(id=id)
    return render(request, 'viewproduct.html',{"products": prds}) 



# from django.http import HttpResponse
# from django.shortcuts import render,redirect
# from django.contrib.auth.models import User, auth
# from django.contrib import messages
# from .forms import NewUserForm
# from django.contrib.auth import login
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login, authenticate,logout


def signup(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request)
			messages.success(request, "Registration successful." )
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="signup.html", context={"register_form":form})




def login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				auth_login(request, user)
				messages.info(request, "You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form}) 



def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")


def productview(request, id):
    prds = Product.objects.get(id=id)
    return render(request, 'productview.html',{"products": prds}) 





def editproduct(request, id):
    global pro
    pro =Product.objects.get(id=id)
    form = ProductForm(instance=pro)
    return render(request, 'productedit.html',{"form":form})

def editproductsave(request):
    if request.method=="POST":
        
        form = ProductForm(request.POST, request.FILES,instance=pro)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'products.html',{"form":form})

def deleteproduct(request, id):
    product=Product.objects.get(id=id)

    product.delete()
    return redirect('/')


class search(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(name__icontains=kw)
        print(results)
        context["results"] = results
        return context    



@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, "Product added to cart.")
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)
    cart_item.delete()
    messages.success(request, "Product removed from cart.")
    return redirect('cart')




@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum([item.product.price * item.quantity for item in cart_items])
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum([item.product.price * item.quantity for item in cart_items])
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                order = Order.objects.create(user=request.user, total_price=total_price, )
                for item in cart_items:
                    order.products.add(item.product)
                order.save()
                messages.success(request, "Order placed successfully.")
                return redirect('order', order_id=order.id)
            except Exception as e:
                messages.error(request, f"Error placing order: {e}")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items, 'total_price': total_price})


@login_required
def order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order.html', {'order': order})



@login_required
def update_cart(request, product_id):
    quantity = request.POST.get('quantity')

    try:
        cart_item = Cart.objects.get(user=request.user, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
    except Cart.DoesNotExist:
        cart_item = Cart.objects.create(
            user=request.user,
            product=Product.objects.get(id=product_id),
            quantity=quantity
        )

    messages.success(request, 'Your cart has been updated.')
    return redirect('cart')
       




def search(request):
    item = request.GET.get('item')
    if item:
        pro = Product.objects.filter(name__icontains=item)
    else:
        pro = Product.objects.none()
    return render(request, "search.html", {"products": pro})
