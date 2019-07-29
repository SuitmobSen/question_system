from django.conf.urls  import url
from . import views

urlpatterns = [
    # 个人资料
    url(r'^profile/$', views.profile, name='profile'),
    # 修改密码
    url(r'^change_passwd/$', views.change_passwd, name='change_passwd'),
    # 我的回答
    url(r'^answer/$', views.answer, name='answer'),
    # 我的收藏
    url(r'^collect/$', views.collect, name='collect'),
    # 我的贡献
    url(r'^contribut/$', views.contribution, name='contribution'),
    # 待审题目
    url(r'^approval/$', views.approval, name='approval'),
    # # 审核题目
    # url(r'^approval/(\d+)/$', views.approval, name='approval_pass'),

]
