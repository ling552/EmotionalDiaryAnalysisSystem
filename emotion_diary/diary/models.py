from django.conf import settings
from django.db import models


class Diary(models.Model):
    EMOTION_CHOICES = [
        ('开心', '开心'),
        ('平静', '平静'),
        ('难过', '难过'),
        ('焦虑', '焦虑'),
        ('未知', '未知'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diaries')
    title = models.CharField(max_length=200)
    content = models.TextField()
    emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES, default='未知')
    score = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self) -> str:
        return f"{self.title} ({self.user})"
