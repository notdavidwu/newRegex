from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Text(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    regexText = models.CharField(max_length=1000)
    inputText = models.CharField(max_length=10000000)

    def __str__(self):
        return str(self.id) + ' | ' + str(self.author)