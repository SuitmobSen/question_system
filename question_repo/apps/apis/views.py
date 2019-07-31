from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from libs import sms
import random
import logging

logger = logging.getLogger("apis")


def get_mobile_captcha(request):
    ret = {"code": 200, "msg": "验证码发送成功！"}
    try:
        mobile = request.GET.get("mobile")
        if mobile is None: raise ValueError("手机号不能为空！")
        mobile_captcha = "".join(random.choices('0123456789', k=6))
        from django.core.cache import cache
        # 将短信验证码写入redis, 300s 过期
        cache.set(mobile, mobile_captcha, 300)
        print(mobile)
        if not sms.send_sms(mobile, mobile_captcha):
            raise ValueError('发送短信失败')
    except Exception as ex:
        logger.error(ex)
        ret = {"code": 400, "msg": "验证码发送失败！"}
    return JsonResponse(ret)


# class Register(View):
#     def get(self, request):
#         form = RegisterForm()
#         return render(request, "accounts/register.html", {"form": form})
#
#     # Ajax提交表单
#     def post(self, request):
#         from django.core.cache import cache
#         ret = {"status": 400, "msg": "调用方式错误"}
#         if request.is_ajax():
#             form = RegisterForm(request.POST)
#             if form.is_valid():
#                 username = form.cleaned_data["username"]
#                 password = form.cleaned_data["password"]
#                 mobile = form.cleaned_data["mobile"]
#                 mobile_captcha = form.cleaned_data["mobile_captcha"]
#                 mobile_captcha_reids = cache.get(mobile)
#                 if mobile_captcha == mobile_captcha_reids:
#                     user = User.objects.create(username=username, password=make_password(password))
#                     user.save()
#                     ret['status'] = 200
#                     ret['msg'] = "注册成功"
#                     logger.debug(f"新用户{user}注册成功！")
#                     user = auth.authenticate(username=username, password=password)
#                     if user is not None and user.is_active:
#                         auth.login(request, user)
#                         logger.debug(f"新用户{user}登录成功")
#                     else:
#                         logger.error(f"新用户{user}登录失败")
#                 else:
#                     # 验证码错误
#                     ret['status'] = 401
#                     ret['msg'] = "验证码错误或过期"
#             else:
#                 ret['status'] = 402
#                 ret['msg'] = form.errors
#         logger.debug(f"用户注册结果：{ret}")
#         return JsonResponse(ret)