from django.conf.urls import url
from . import views

urlpatterns = [
    # 注册
    url(r'register/$', views.register, name="register"),
    # 登录
    url(r'login/$', views.login, name="login"),
    # 退出
    url(r'logout/$', views.logout, name="logout"),
    # 忘记密码
    url(r'password/forget/$', views.password, name="password_forget"),
    # 重置密码
    url(r'password/reset/token/$', views.reset, name="password_reset"),
]
