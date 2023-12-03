from django.db import models

# Create your models here.
class EmailBase(models.Model):
    id=models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254,unique=True)
    def __str__(self):
        return self.email
