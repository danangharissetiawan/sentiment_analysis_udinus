from django.db import models


class Broadcast(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    message = models.TextField()
    classification = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.email