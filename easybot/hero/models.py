from __future__ import unicode_literals

from django.db import models
import uuid


class Bot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='')
    api_key = models.CharField(max_length=500, default='')


class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=100, default='')
    text = models.CharField(max_length=5000, default='')

    def __str__(self):
        return self.text


class Entity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=5000, default='')
    response = models.ForeignKey(Response)

    def __str__(self):
        return self.text


class Intent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=5000, default='')

    bot = models.ForeignKey(Bot, related_name='intent')
    entity = models.ManyToManyField(Entity, related_name='intent')
    response = models.ForeignKey(Response, related_name='intent')

    class Meta:
        unique_together = ('text', 'bot')

    def __str__(self):
        return self.text
