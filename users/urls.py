from django.urls import path,include
from .views import ProductView,RegisterView, LoginView,ForgetPassView,RazorpayView,CartView,AddressView,PaymentView,OrderView,ForgetChangePassView,ChangePassword,ReviewView
from rest_framework.routers import DefaultRouter
#, UserView, LogoutView,CartCreateView,

route = DefaultRouter()
route.register("product",ProductView,basename='productview')
route.register("address",AddressView,basename='adressview')
route.register("cart",CartView,basename='cartview')
route.register("payment",PaymentView,basename='paymentview')
route.register("order",OrderView,basename='orderview')
route.register("review",ReviewView,basename='reviewview')


urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('forgetpass',ForgetPassView.as_view()),
    path("order/create", RazorpayView.order_payment, name="create"),
    # path("callback/", callback, name="callback"),
    path('forgetchangepass/<pk>',ForgetChangePassView.as_view()),
    path('changepass/<pk>',ChangePassword.as_view()),
    path('',include(route.urls)),
    # path('cartdetail/<int:pk>/',CartView.as_view()),
    # path('user',UserView.as_view()),
    # path('logout',LogoutView.as_view()),
]