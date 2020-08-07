from django.urls import path, re_path

from App import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('market/', views.market, name='market'),
    re_path('marketwithparams/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/', views.market_with_params,
            name='market_with_params'),
    path('cart/', views.cart, name='cart'),
    path('mine/', views.mine, name='mine'),
    re_path('register/', views.register, name='register'),
    re_path('login/', views.login, name='login'),
    re_path('checkuser/', views.checkuser, name='checkuser'),
    re_path('checkemail/', views.checkemail, name='checkemail'),
    path('loginout/', views.login_out, name='login_out'),
    path('emailactivate/', views.email_activate, name='email_activate'),
    path('addtocart/',views.add_to_cart,name='add_to_cart'),
    path('subtocart/',views.sub_to_cart,name='sub_to_cart'),
    path('changecartstate/',views.change_cart_state,name='change_cart_state'),
    path('allselect/',views.all_select,name='all_select'),
    path('makeorder/',views.make_order,name='make_order'),
    path('orderdetail/',views.order_detail,name='order_detail'),
    path('orderlistnotpay/',views.order_list_not_pay,name='order_list_not_pay'),
    path('payed/',views.payed,name='payed'),


]

