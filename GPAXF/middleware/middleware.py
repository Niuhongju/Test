from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import AXFUser

REQUIRE_LOGIN_JSON=[
    '/axf/addtocart/',
    '/axf/subtocart/',
    '/axf/changecartstate/',
    '/axf/allselect/',
    '/axf/makeorder/',
]
REQUIRE_LOGIN=[
    '/axf/cart/',
    '/axf/orderdetail/',
    # '/axf/mine/',
    '/axf/orderlistnotpay/',
]
class LoginMiddleware(MiddlewareMixin):
    def process_request(self,request):
        if request.path in REQUIRE_LOGIN_JSON:
            user_id=request.session.get('user_id')
            if user_id:
                user=AXFUser.objects.get(pk=user_id)
                request.user=user
            else:
                data={
                    'status':302,
                    'msg':'not login',
                }
                return JsonResponse(data)
        if request.path in REQUIRE_LOGIN:
            user_id = request.session.get('user_id')
            # if user_id:
            #     user = AXFUser.objects.get(pk=user_id)
            #     request.user = user
            # else:
            #     data = {
            #         'status': 302,
            #         'msg': 'not login',
            #     }
            #     return JsonResponse(data)
            if not user_id:
                return redirect(reverse('axf:login'))
            else:
                user = AXFUser.objects.get(pk=user_id)
                request.user = user
