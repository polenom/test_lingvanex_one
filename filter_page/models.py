from django.db import models

# Create your models here.

class App(models.Model):
    name_app = models.CharField(max_length=200, unique=True)
    company = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    release = models.DateTimeField()

    def __str__(self):
        return str(self.name_app)