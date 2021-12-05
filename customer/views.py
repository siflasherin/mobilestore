from django.shortcuts import render, redirect
from customer import forms
from django.contrib.auth import authenticate, login, logout
from mobile.models import Mobile, Cart, Orders
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from mobile.decorators import signin_required,admin_permission_required
from django.utils.decorators import method_decorator
from django.db.models import Sum
from customer.filters import MobileFilter
import django_filters

# Create your views here.

# def customer_home(request):
#     mobiles=Mobile.objects.all()
#     context={}
#     context["mobiles"]=mobiles
#     return render(request, "customer/home.html",context)
@method_decorator(signin_required,name="dispatch")
class CustomerHome(TemplateView):
    def get(self, request, *args, **kwargs):
        mobiles = Mobile.objects.all()
        context = {}
        context["mobiles"] = mobiles
        return render(request, "customer/home.html", context)


# def sign_up(request):
#     form = forms.UserRegistrationForm()
#     context = {"form": form}
#     # context["form"] = form
#     if request.method == "POST":
#         form = forms.UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print("user has been registered")
#             return redirect("signin")
#         else:
#             context["form"] = form
#             return render(request, "user_registration.html", context)
#     return render(request, "user_registration.html", context)


class SignUp(TemplateView):
    def get(self, request, *args, **kwargs):
        form = forms.UserRegistrationForm()
        context = {"form": form}
        return render(request, "user_registration.html", context)

    def post(self, request):
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("user has been registered")
            return redirect("signin")
        else:
            context = {"form": form}
            return render(request, "user_registration.html", context)


# def signin(request):
#     form = forms.LoginForm()
#     context = {}
#     context["form"] = form
#     if request.method == "POST":
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect("customerhome")
#             else:
#                 return render(request, "login.html", {"form": form})
#     return render(request, "login.html", context)

class SignIn(TemplateView):
    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        context = {}
        context["form"] = form
        return render(request, "login.html", context)

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("customerhome")
            else:
                return render(request, "login.html", {"form": form})


@signin_required
def signout(request):
    logout(request)
    return redirect("signin")


@method_decorator(signin_required,name="dispatch")
class AddToCart(TemplateView):
    model = Cart

    def get(self, request, *args, **kwargs):
        id = kwargs["id"]
        mobile = Mobile.objects.get(id=id)
        cart = Cart.objects.create(item=mobile, user=request.user)
        # print("item is added to cart")
        messages.success(request, "item added to cart")
        cart.save()
        return redirect("customerhome")


@method_decorator(signin_required,name="dispatch")
class MyCart(TemplateView):
    model = Cart
    template_name = "mycart.html"
    context = {}

    def get(self, request, *args, **kwargs):
        mycart = self.model.objects.filter(user=request.user, status="incart")
        self.context["items"] = mycart
        total=Cart.objects.filter(user=request.user,status="incart").aggregate(Sum("item__price"))
        self.context["total"] = total["item__price__sum"]
        return render(request, self.template_name, self.context)


@method_decorator(signin_required,name="dispatch")
class RemoveItem(TemplateView):
    model = Cart

    def get(self, request, *args, **kwargs):
        id = kwargs["id"]
        cart = Cart.objects.get(id=id)
        cart.status = "cancelled"
        cart.save()
        messages.success(request, "item has been removed from cart")
        return redirect("customerhome")


@method_decorator(signin_required,name="dispatch")
class OrderCreate(TemplateView):
    model = Orders
    form_class = forms.OrderForm
    template_name = "ordercreation.html"
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context["form"] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        cid = kwargs["id"]
        cart_item = Cart.objects.get(id=cid)
        form = self.form_class(request.POST)
        if form.is_valid():
            address = form.cleaned_data["address"]
            user = request.user.username

            order = Orders.objects.create(
                address=address,
                item=cart_item,
                user=user,
            )
            order.save()
            cart_item.status = "orderplaced"
            cart_item.save()
            messages.success(request, "your order has been placed")
            return redirect("customerhome")


# class MyOrders(TemplateView):
#     model = Orders
#     template_name = "myorders.html"
#     context = {}
#
#     def get(self, request, *args, **kwargs):
#         myorder = self.model.objects.filter(user=request.user, status="orderplaced")
#         self.context["items"] = myorder
#         return render(request, self.template_name, self.context)


@method_decorator(signin_required,name="dispatch")
class ViewMyOrder(ListView):
    model = Orders
    template_name = "myorders.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset


class MobileSearch(TemplateView):
    model=Mobile
    template_name = "base.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        f=MobileFilter(self.request.GET,queryset=Mobile.objects.all())
        context["filter"]=f
        return context


# item = cart_item.item
#             order = self.model.objects.create(
#                 address=address,
#                 item=item,
#                 user=user,
