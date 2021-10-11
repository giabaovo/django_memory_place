from django.db import models
from django.contrib.gis.db import models

from django.urls import reverse

from users.models import User


class Memory(models.Model):
    name = models.CharField(max_length=100)
    descripsion = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='memory')
    location = models.PointField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("memory_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = 'Memories'
