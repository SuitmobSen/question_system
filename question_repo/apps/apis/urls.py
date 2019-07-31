from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^get_mobile_captcha/$", views.get_mobile_captcha, name="get_mobile_captcha")
]