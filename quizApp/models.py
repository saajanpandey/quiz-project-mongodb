# from django.db import models

# Create your models here.
# from django.db import models
from djongo import models
from django.contrib.auth.models import User


# Model to store questions
class Question(models.Model):
    text = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.text


# Model to store quiz results
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    percentage = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz Result for {self.user.first_name}  {self.user.last_name} on {self.date_taken}"
