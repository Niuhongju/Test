import hashlib

from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import loader

from App.models import Cart
from GPAXF.settings import SERVER_HOST, SERVER_PORT


def has_str(source):
    return hashlib.new('sha512',source.encode('utf-8')).hexdigest()

def send_email_activate(username,receive_email,u_token):
    subject='AXF Activate'
    data={
        'username':username,
        'activate_url':'http://{}:{}/axf/emailactivate/?u_token={}'.format(SERVER_HOST,SERVER_PORT,u_token)
    }
    html_message =loader.get_template('user/activate.html').render(data)
    from_email='619696982@qq.com'
    recipient_list=[receive_email]
    send_mail(subject=subject,message='XXX',from_email=from_email,recipient_list=recipient_list,html_message=html_message)
    return HttpResponse('邮件发送成功')

def get_total_price(user):
    carts=Cart.objects.filter(c_is_select=True).filter(c_user=user)
    total_price=0
    for cart in carts:
        total_price+=cart.c_goods_num*cart.c_goods.price
    return "{:.2f}".format(total_price)