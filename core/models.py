from django.contrib.auth.models import User
from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500)
    creator = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    number_of_likes = models.PositiveIntegerField(default=0)
    number_of_comments = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('created', )


class Comment(models.Model):
    body = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('created', )


class TopicLike(models.Model):
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name='topic_likes', on_delete=models.CASCADE)

