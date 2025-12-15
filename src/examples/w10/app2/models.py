from django.db import models

class App2Model(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["created"]
