import uuid
from asyncio import sleep

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import caches, cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, AXFUser, Cart, Order, \
    OrderGoods

# from App.views_constant import ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN
from App.views_constant import HTTP_CHECK_OK, HTTP_CHECK_EXIST, ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_RECEIVE, \
    ORDER_STATUS_NOT_SEND
from App.views_helper import has_str, send_email_activate, get_total_price
from GPAXF.settings import MEDIA_KEY_PREFIX


def home(request):
    main_wheels=MainWheel.objects.all()
    main_navs=MainNav.objects.all()
    main_mustbuys=MainMustBuy.objects.all()
    main_shop=MainShop.objects.all()
    main_shop0_1=main_shop[0:1]
    main_shop1_3=main_shop[1:3]
    main_shop3_7=main_shop[3:7]
    main_shop7_11=main_shop[7:11]
    main_shows=MainShow.objects.all()
    data={
        'title':'首页',
        'main_wheels':main_wheels,
        'main_navs':main_navs,
        'main_buys':main_mustbuys,
        'main_shop0_1':main_shop0_1,
        'main_shop1_3':main_shop1_3,
        'main_shop3_7':main_shop3_7,
        'main_shop7_11':main_shop7_11,
        'main_shows':main_shows,
    }
    return render(request,'main/home.html',context=data)


def market(request):
    return  redirect(reverse('axf:market_with_params',kwargs={
        'typeid':104749,
        'childcid':0,
        'order_rule':0,
    }))
    # pass

def market_with_params(request,typeid,childcid,order_rule):
    print(order_rule)
    print(type(order_rule))
    foodtypes=FoodType.objects.all()
    if int(childcid):
        goods_list=Goods.objects.filter(categoryid=typeid).filter(childcid=childcid)
        for good in goods_list:
            childcidname = good.childcidname
    else:
        goods_list=Goods.objects.filter(categoryid=typeid)
        childcidname ='全部分类'

    if order_rule=='0':
        pass
    elif order_rule=='1':
        goods_list=goods_list.order_by('price')
    elif order_rule=='2':
        goods_list=goods_list.order_by('-price')
    elif order_rule=='3':
        goods_list=goods_list.order_by('productnum')
    elif order_rule=='4':
        goods_list=goods_list.order_by('-productnum')
    order_rule_list=[
        ['综合排序',0],
        ['价格升序',1],
        ['价格降序',2],
        ['销量升序',3],
        ['销量降序',4],
    ]
    for order_rules in order_rule_list:
        if order_rules[1]==int(order_rule):
            order_rule_name=order_rules[0]
    foodtype=FoodType.objects.get(typeid=typeid)
    foodtypechildnames=foodtype.childtypenames
    '''
    对食物种类名字的子名字进行切割。
    如：将优选水果所包含的子种类分为进口水果，国产水果
    得到如[[进口水果：103534],[国产水果：103533]]形式的
    '''
    foodtypechildname_list=foodtypechildnames.split('#')
    foodtype_childname_list=[]
    for foodtypechildname in foodtypechildname_list:
        foodtype_childname_list.append(foodtypechildname.split(':'))

    data={
        'title':'闪购',
        'foodtypes':foodtypes,
        'goods_list':goods_list,
        'typeid':int(typeid),
        'foodtype_childname_list':foodtype_childname_list,
        'childcid':childcid,
        'order_rule_list':order_rule_list,
        'order_rule':int(order_rule),
    }
    return render(request,'main/market.html',context=data)


def cart(request):

    carts=Cart.objects.filter(c_user=request.user)

    is_all_select=carts.filter(c_is_select=False).exists()

    data={
        'title':'购物车',
        'carts':carts,
        'is_all_select':is_all_select,
        'total_price':get_total_price(request.user),
    }
    return render(request,'main/cart.html',context=data)


def mine(request):
    user_id=request.session.get('user_id')
    user = AXFUser.objects.filter(id=user_id).first()
    data = {
        'title': '我的',
        'is_login': False,
    }

    if user_id:
        data['username']=user.u_username
        data['icon']=MEDIA_KEY_PREFIX + user.u_icon.url
        data['is_login']=True
        data['order_status_not_pay_num']=Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_status_not_receive_num']=Order.objects.filter(o_user=user).filter(o_status__in=(ORDER_STATUS_NOT_RECEIVE,ORDER_STATUS_NOT_SEND)).count()

    return render(request,'main/mine.html',context=data)

@csrf_exempt
def register(request):
    if request.method=='GET':
        data={
            'title':'注册'
        }
        return render(request,'user/register.html',context=data)
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        icon=request.FILES.get('icon')

        # password=has_str(password)
        password=make_password(password)

        user=AXFUser()
        user.u_username=username
        user.u_email=email
        user.u_password=password
        user.u_icon=icon
        user.save()
        u_token=uuid.uuid4().hex
        cache=caches['redis_backend']
        cache.set(u_token,user.id,timeout=60*60*24)
        receive_email=email
        send_email_activate(username,receive_email,u_token)
        return HttpResponse('注册成功，请前往邮箱进行激活')

# @cache_page(60,cache='redis_backend')
def email_activate(request):
    u_token=request.GET.get('u_token')
    cache = caches['redis_backend']
    user_id=cache.get(u_token)
    cache.delete(u_token)
    user=AXFUser.objects.get(pk=user_id)
    user.is_active=True
    user.save()
    return render(request, 'user/activate_success.html')
    # return HttpResponse('激活成功')


@csrf_exempt
def login(request):
    error_message=request.session.get('error_message')
    if request.method=='GET':
        data={
            'title':'登录',
        }
        if error_message:
            del request.session['error_message']
            data['error_message']=error_message
        return render(request, 'user/login.html', context=data)
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        users=AXFUser.objects.filter(u_username=username)
        if users:
            user=users.first()
            if check_password(password,user.u_password):
                if user.is_active:
                    request.session['user_id']=user.id
                    return redirect(reverse('axf:mine'))
                else:
                    request.session['error_message'] = '邮箱未激活，进行激活'

            else:
                request.session['error_message']='密码错误'
                return redirect(reverse('axf:login'))
        else:
            request.session['error_message']='用户不存在'
        return redirect(reverse('axf:login'))

def login_out(request):
    request.session.flush()
    return redirect(reverse('axf:mine'))


def checkuser(request):
    username=request.GET.get('username')
    user=AXFUser.objects.filter(u_username=username)
    print(user)
    data={
        'status':HTTP_CHECK_OK,
    }
    if user:
        data['status']=HTTP_CHECK_EXIST
    else:
        pass
    return JsonResponse(data=data)


def checkemail(request):
    email=request.GET.get('email')
    user=AXFUser.objects.filter(u_email=email)
    print(email)
    data = {
        'status': HTTP_CHECK_OK
    }
    if user:
        data={
            'status':HTTP_CHECK_EXIST
        }
    else:
        pass
    return JsonResponse(data=data)


def add_to_cart(request):
    goodsid=request.GET.get('goodsid')
    user=request.user
    carts=Cart.objects.filter(c_goods_id=goodsid).filter(c_user=request.user)

    if carts:
        cart=carts.first()
        cart.c_goods_num=cart.c_goods_num+1
    else:
        cart=Cart()
        cart.c_user=request.user
        # good=Goods.objects.get(goodsid=goodsid)
        # cart.c_goods=good
        cart.c_goods_id=goodsid
        cart.c_goods_num=1
    cart.save()
    data={
        'status':200,
        'msg':'添加成功',
        'c_good_num':cart.c_goods_num,
        'total_price': get_total_price(request.user),
    }
    return JsonResponse(data)


def sub_to_cart(request):
    goodsid=request.GET.get('goodsid')
    user=request.user
    carts=Cart.objects.filter(c_goods_id=goodsid).filter(c_user=request.user)

    if carts:
        cart=carts.first()
        cart.c_goods_num=cart.c_goods_num-1
        cart.save()
        data={
            'status':200,
            'msg':'减少成功',
            'c_good_num':cart.c_goods_num,
            'total_price': get_total_price(request.user),
        }
        if cart.c_goods_num==0:
            cart.delete()

    return JsonResponse(data)


def change_cart_state(request):

    cartid=request.GET.get('cartid')

    cart=Cart.objects.get(pk=cartid)

    cart.c_is_select=not cart.c_is_select

    cart.save()

    is_all_select= not Cart.objects.filter(c_user=request.user).filter(c_is_select=False)


    data={
        'status':200,
        'msg':'状态改变成功',
        'c_is_select':cart.c_is_select,
        'is_all_select':is_all_select,
        'total_price': get_total_price(request.user),

    }
    return JsonResponse(data)


def all_select(request):

    cart_list=request.GET.get('cart_list')

    cart_list=cart_list.split('#')

    print(cart_list)

    carts=Cart.objects.filter(id__in=cart_list )

    for cart in carts:
        cart.c_is_select=not cart.c_is_select
        cart.save()
    data={
        'status':200,
        'msg':'全选操作成功',
        'total_price': get_total_price(request.user),
    }
    return JsonResponse(data)


def make_order(request):

    carts=Cart.objects.filter(c_user=request.user).filter(c_is_select=True)

    order=Order()

    order.o_user=request.user

    order.o_price=get_total_price(request.user)

    order.save()

    for cart in carts:
        ordergoods=OrderGoods()
        ordergoods.o_order=order
        ordergoods.o_goods=cart.c_goods
        ordergoods.o_goods_num=cart.c_goods_num
        ordergoods.save()
        cart.delete()

    data={
        'status':200,
        'msg':'生成订单',
        'order_id':order.id,
    }
    return JsonResponse(data)


def order_detail(request):

    order_id=request.GET.get('orderid')

    order=Order.objects.get(pk=order_id)

    data={
        'title':'订单详情',
        'order':order,
    }
    return render(request,'order/order_detail.html',context=data)


def order_list_not_pay(request):

    orders=Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_PAY)

    data={
        'title':'订单列表',
        'orders':orders,
    }
    return render(request,'order/order_list_not_pay.html',context=data)


def payed(request):
    orderid=request.GET.get('orderid')

    order=Order.objects.get(pk=orderid)

    order.o_status=ORDER_STATUS_NOT_SEND

    order.save()
    data={
        'status':200,
        'msg':'付款成功',
    }
    return JsonResponse(data)