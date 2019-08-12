from django.db import models

# Create your models here.
from apps.accounts.models import User
from .validator import valid_difficulty
from ckeditor.fields import RichTextField
# 含文件上传
from ckeditor_uploader.fields import RichTextUploadingField



class Category(models.Model):
    """分类"""
    name = models.CharField("分类名称", max_length=64)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField("标签名", max_length=64)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class Questions(models.Model):
    """题库"""
    DIF_CHOICES = (
        (1, "入门"),
        (2, "简单"),
        (3, "中等"),
        (4, "困难"),
        (5, "超难"),
    )
    grade = models.IntegerField("题目难度", choices=DIF_CHOICES, validators=[valid_difficulty], null=True)
    category = models.ForeignKey(Category, verbose_name="所属分类", null=True)
    title = models.CharField("题目标题", unique=True, max_length=256)
    # 富文本编辑器
    # content = models.TextField("题目详情", null=True)
    content = RichTextUploadingField("题目详情", null=True)
    # 富文本编辑器
    # answer = models.TextField("题目答案", null=True, blank=True)
    answer = RichTextUploadingField("题目答案", null=True, blank=True)
    contributor = models.ForeignKey(User, verbose_name="贡献者", null=True)
    pub_time = models.DateTimeField("入库时间", auto_now_add=True, null=True)
    # 审核状态
    status = models.BooleanField("审核状态", default=False)
    # 数组....(会产生一个中间表)
    tag = models.ManyToManyField(Tag, verbose_name="题目标签")

    class Meta:
        verbose_name = "题库"
        verbose_name_plural = verbose_name
        permissions = (
                        ('can_change_question', "可以修改题目信息"),
                       ('can_add_question', "可以添加题目信息"),
                       )

    def __str__(self):
        return f"{self.id}:{self.title}"


class QuestionsCollection(models.Model):
    """收藏问题"""
    question = models.ForeignKey(Questions, verbose_name="问题", related_name='questions_collection_set')
    user = models.ForeignKey(User, verbose_name="收藏者", related_name='questions_collection_set')
    create_time = models.DateTimeField("收藏/取消时间", auto_now=True)
    # True表示收藏 ,False表示未收藏
    status = models.BooleanField("收藏状态", default=True)

    class Meta:
        verbose_name = "题目收藏记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.status:
            ret = "收藏"
        else:
            ret = "取消收藏"
        return f"{self.user}:{ret}:{self.question.title}"


class Answers(models.Model):
    """答题记录"""
    # objects = AnswersManager()
    # exam = models.ForeignKey(ExamQuestions, verbose_name="所属试卷", null=True, blank=True)
    question = models.ForeignKey(Questions, verbose_name="题目")
    answer = models.TextField(verbose_name="学生答案")
    user = models.ForeignKey(User, verbose_name="答题人")
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "答题记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user}-{self.question.title}"

    # def to_dict(self):
    #     return dict([(attr, getattr(self, attr)) for attr in
    #                  [f.name for f in self._meta.fields]])
    #     # type(self._meta.fields).__name__


class AnswersCollection(models.Model):
    """收藏答案"""
    answer = models.ForeignKey(Answers, verbose_name="答题记录", related_name='answers_collection_set')
    user = models.ForeignKey(User, verbose_name="收藏者", related_name='answers_collection_set')
    create_time = models.DateTimeField("收藏/取消时间", auto_now=True)
    # True表示收藏 ,False表示未收藏
    status = models.BooleanField("收藏状态", default=True)

    class Meta:
        verbose_name = "答案收藏记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.status: ret="收藏"
        else: ret="取消收藏"
        return f"{self.user}:{ret}:{self.answer}"