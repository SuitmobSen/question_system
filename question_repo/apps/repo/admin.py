from django.contrib import admin

# Register your models here.

from .models import Category, Tag, Questions, QuestionsCollection, AnswersCollection, Answers

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Questions)
admin.site.register(QuestionsCollection)
admin.site.register(AnswersCollection)
admin.site.register(Answers)

