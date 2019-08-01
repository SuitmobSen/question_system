from django.conf.urls import url
from . import views


urlpatterns = [
    # 短信验证码
    url(r"^get_mobile_captcha/$", views.get_mobile_captcha, name="get_mobile_captcha"),
    # 图片验证码
    url(r"^get_captcha/$", views.get_captcha, name='get_captcha'),
    # 验证码检查接口
    url(r"^check_captcha$", views.check_captcha, name="check_captcha")
]