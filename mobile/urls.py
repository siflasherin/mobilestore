from django.urls import path
from mobile import views

urlpatterns = [
    path("", views.home, name="home"),
    path("mobile/add", views.AddMobile.as_view(), name="addmobile"),
    path("mobile/list", views.ListMobile.as_view(), name="listmobile"),
    path("remove<int:id>", views.RemoveMobile.as_view(), name="removemobile"),
    path("update<int:id>", views.UpdateMobile.as_view(), name="updatemobile"),
    path("view<int:id>", views.ViewMobile.as_view(), name="mobileview"),
    path("cusrorders", views.ViewOrders.as_view(), name="customerorders"),
    path("customerorderview<int:id>", views.DetailCusView.as_view(), name="cusorderview"),
    path("customerorderupdate<int:id>", views.OrderUpdateView.as_view(), name="customerorderupdate"),
    path("accounts/signout", views.signout, name="signout"),
    path("find",views.MobileSearch.as_view(),name="mobilefilter"),
    path("adminlogin",views.SignIn.as_view(),name="login"),
]
