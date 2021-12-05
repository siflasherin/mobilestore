from django.shortcuts import render, redirect
from mobile.forms import MobileAddForm,OrderUpdateForm,LoginForm
from mobile.models import Mobile, Orders
from django.views.generic import TemplateView, CreateView, DetailView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from mobile.decorators import signin_required,admin_permission_required
from django.contrib.auth import logout,login,authenticate
from mobile.filters import MobileFilter

# Create your views here.

def home(request):
    return render(request, "home.html")


# def add_mobile(request):
#     if request.method == "GET":
#         form = MobileAddForm()
#
#         context = {}
#         context["form"] = form
#
#         return render(request, "add_mobile.html", context)
#
#     if request.method == "POST":
#         form = MobileAddForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             form.save()
#             # m_name = form.cleaned_data["mobile_name"]
#             # model = form.cleaned_data["model"]
#             # color = form.cleaned_data["colour"]
#             # ram = form.cleaned_data["storage"]
#             # copies = form.cleaned_data["copies"]
#             # price = form.cleaned_data["price"]
#             # mobile = Mobile.objects.create(mobile_name=m_name, model=model, colour=color, storage=ram, copies=copies,
#             #                                price=price)
#             # mobile.save()
#             # print("New Mobile Saved Succsessfully....")
#             # # print(m_name,model,color,ram,copies,price)
#             return redirect("listmobile")
#         else:
#             return render(request, "add_mobile.html", {"form": form})
#             # context


# class AddMobile(TemplateView):
#     def get(self, request, *args, **kwargs):
#         form = MobileAddForm()
#         context = {}
#         context["form"] = form
#         return render(request, "add_mobile.html", context)
#
#     def post(self, request):
#         form = MobileAddForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("listmobile")
#         else:
#             return render(request, "add_mobile.html", {"form": form})

@method_decorator(signin_required,name="dispatch")
class AddMobile(CreateView):
    model = Mobile
    form_class = MobileAddForm
    template_name = "add_mobile.html"
    success_url = reverse_lazy("listmobile")


# def list_mobile(request):
#     mobiles = Mobile.objects.all()
#     # mobiles.save()
#     context = {}
#     context["mobiles"] = mobiles
#     return render(request, "list_mobile.html", context)

# class ListMobile(TemplateView):
#     def get(self, request, *args, **kwargs):
#         mobiles = Mobile.objects.all()
#         context = {}
#         context["mobiles"] = mobiles
#         return render(request, "list_mobile.html", context)

@method_decorator(signin_required,name="dispatch")
class ListMobile(ListView):
    model = Mobile
    template_name = "list_mobile.html"
    context_object_name = "mobiles"


# def remove_mobile(request, id):
#     mobile = Mobile.objects.get(id=id)
#     mobile.delete()
#     return redirect("listmobile")


# class RemoveMobile(TemplateView):
#     def get(self, request, *args, **kwargs):
#         id = kwargs["id"]
#         mobile = Mobile.objects.get(id=id)
#         mobile.delete()
#         return redirect("listmobile")


@method_decorator(signin_required,name="dispatch")
class RemoveMobile(DeleteView):
    model = Mobile
    template_name = "remove_mobile.html"
    success_url = reverse_lazy("listmobile")
    pk_url_kwarg = "id"


# def update_mobile(request, id):
#     mobile = Mobile.objects.get(id=id)
#     if request.method == "GET":
#         form = MobileAddForm(instance=mobile)
#         #     initial={
#         #     "mobile_name": mobile.mobile_name,
#         #     "model": mobile.model,
#         #     "colour": mobile.colour,
#         #     "storage": mobile.storage,
#         #     "copies": mobile.copies,
#         #     "price": mobile.price,
#         # }
#
#         context = {}
#         context["form"] = form
#         return render(request, "update_mobile.html", context)
#     if request.method == "POST":
#         form = MobileAddForm(request.POST, instance=mobile)
#         if form.is_valid():
#             form.save()
#             # m_name = form.cleaned_data["mobile_name"]
#             # model = form.cleaned_data["model"]
#             # color = form.cleaned_data["colour"]
#             # ram = form.cleaned_data["storage"]
#             # copies = form.cleaned_data["copies"]
#             # price = form.cleaned_data["price"]
#             #
#             # mobile.mobile_name = m_name
#             # mobile.model = model
#             # mobile.colour = color
#             # mobile.storage = ram
#             # mobile.copies = copies
#             # mobile.price = price
#             # mobile.save()
#             return redirect("listmobile")


# class UpdateMobile(TemplateView):
#     def get(self, request, *args, **kwargs):
#         id = kwargs["id"]
#         mobile = Mobile.objects.get(id=id)
#         form = MobileAddForm(instance=mobile)
#         context = {}
#         context["form"] = form
#         return render(request, "update_mobile.html", context)
#
#     def post(self, request, *args, **kwargs):
#         id = kwargs["id"]
#         mobile = Mobile.objects.get(id=id)
#         form = MobileAddForm(request.POST, instance=mobile)
#         if form.is_valid():
#             form.save()
#             return redirect("listmobile")

@method_decorator(signin_required,name="dispatch")
class UpdateMobile(UpdateView):
    model = Mobile
    template_name = "update_mobile.html"
    form_class = MobileAddForm
    pk_url_kwarg = "id"
    success_url = reverse_lazy("listmobile")


# def view_mobile(request, id):
#     mobile = Mobile.objects.get(id=id)
#     context = {}
#     context["mobile"] = mobile
#     return render(request, "view_mobile.html", context)


# class ViewMobile(TemplateView):
#     def get(self, request, *args, **kwargs):
#         id = kwargs["id"]
#         mobile = Mobile.objects.get(id=id)
#         context = {}
#         context["mobile"] = mobile
#         return render(request, "view_mobile.html", context)

@method_decorator(signin_required,name="dispatch")
class ViewMobile(DetailView):
    model = Mobile
    template_name = "view_mobile.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("listmobile")

@method_decorator(signin_required,name="dispatch")
class ViewOrders(ListView):
    model = Orders
    template_name = "customer_orders.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        neworder = self.model.objects.filter(status="orderplaced")
        context["neworder"] = neworder
        context["new_order_count"] = neworder.count()

        d_order = self.model.objects.filter(status="delivered")
        context["d_order"] = d_order
        context["d_order_count"] = d_order.count()

        return context

@method_decorator(signin_required,name="dispatch")
class DetailCusView(DetailView):
    model = Orders
    template_name = "cus_order_view.html"
    context_object_name = "order"
    pk_url_kwarg = "id"

@method_decorator(signin_required,name="dispatch")
class OrderUpdateView(UpdateView):
    model=Orders
    form_class=OrderUpdateForm
    template_name = "order_update.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("customerorders")



class SignIn(TemplateView):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {}
        context["form"] = form
        return render(request, "adminlogin.html", context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("addmobile")
            else:
                return render(request, "adminlogin.html", {"form": form})


@signin_required
def signout(request):
    logout(request)
    return redirect("login")


@method_decorator(signin_required,name="dispatch")
class MobileSearch(TemplateView):
    model=Mobile
    template_name = "mobiles.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        f=MobileFilter(self.request.GET,queryset=Mobile.objects.all())
        context["filter"]=f
        return context