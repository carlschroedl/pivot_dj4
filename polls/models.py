from django.db import models
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self) -> str:
        return self.question_text

    def was_published_recently(self) -> str:
        now = timezone.now()
        recent_window = now - datetime.timedelta(days=1)
        was_published_recently = recent_window <= self.pub_date and self.pub_date <= now
        return was_published_recently

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text


