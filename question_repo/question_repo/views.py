from django.shortcuts import render, HttpResponse
import logging

# Create your views here.


logger = logging.getLogger("apis")

def logtest(request):
    logger.info("欢迎访问")
    return  HttpResponse("日志测试")