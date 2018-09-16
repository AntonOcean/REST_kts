from django.contrib import admin

from core.models import Comment, Topic

admin.site.register((Topic, Comment))

