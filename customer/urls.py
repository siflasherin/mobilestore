from django.urls import path
from customer import views

urlpatterns = [
    path("home", views.CustomerHome.as_view(), name="customerhome"),
    path("accounts/users/add", views.SignUp.as_view(), name="signup"),
    path("accounts/users/signin", views.SignIn.as_view(), name="signin"),
    path("accounts/users/signout", views.signout, name="signout"),
    path("mobiles/addtocart<int:id>",views.AddToCart.as_view(),name="addtocart"),
    path("mobiles/mycart",views.MyCart.as_view(),name="mycart"),
    path("mobiles/removeitem<int:id>",views.RemoveItem.as_view(),name="removeitem"),
    path("mobiles/buynow<int:id>",views.OrderCreate.as_view(),name="ordercreation"),
    path("mobile/myorders",views.ViewMyOrder.as_view(),name="myorders"),
]
