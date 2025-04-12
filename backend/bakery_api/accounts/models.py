from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'users'  
        managed = False     