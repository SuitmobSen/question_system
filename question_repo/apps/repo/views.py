from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Questions, Category, Answers
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import logging
from django.http import JsonResponse
from django.core import serializers
from django.db import transaction
# Create your views here.

logger = logging.getLogger("repo")

def test(request):
    return HttpResponse("题库视图")


# # 要求用户需要登录了才能访问该页面，如果没有登录，跳转到 ==》/accounts/login
# @login_required()
def index(request):
    return render(request, "index.html")


class QuestionsList(View):
    def get(self, request):
        category = Category.objects.all().values("id", "name")
        grades = Questions.DIF_CHOICES
        search = request.GET.get("search", "")
        kwgs = {"category": category, "grades": grades, "search": search}
        return render(request, 'bak/question.html', kwgs)


class QuestionDetail(DetailView):
    model = Questions
    pk_url_kwarg = 'id'
    template_name = "question_detail.html"
    # 额外传递my_answer
    def get_context_data(self, **kwargs):
        # kwargs：字典、字典中的数据返回给html页面
        # self.get_object() => 获取当前id的数据（问题）
        question = self.get_object()  # 当前这道题目
        kwargs["my_answer"] = Answers.objects.filter(question=question, user=self.request.user)
        return super().get_context_data(**kwargs)

    def post(self, request, id):
        try:
            # 没有回答过。create
            # 更新回答。get->update
            # 获取对象，没有获取到直接创建对象
            new_answer = Answers.objects.get_or_create(question=self.get_object(), user=self.request.user)
            # 元组：第一个元素获取/创建的对象， True（新创建）/False（老数据）
            new_answer[0].answer = request.POST.get("answer", "没有提交答案信息")
            new_answer[0].save()
            my_answer = json.loads(serializers.serialize("json", [new_answer[0]]))[0]["fields"]
            msg = "提交成功"
            code = 200
        except Exception as ex:
            logger.error(ex)
            my_answer = {}
            msg = "提交失败"
            code = 500
        result = {"status": code, "msg": msg, "my_answer": my_answer}
        return JsonResponse(result)


