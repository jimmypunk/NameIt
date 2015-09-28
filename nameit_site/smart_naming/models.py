from django.db import models
from django.contrib.postgres import fields
from jsonfield import JSONField


class Repo(models.Model):
    repo_url = models.URLField()
    repo_info = JSONField(default="")


class RepoWordCountView(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    total = models.IntegerField(default=0)
    files = fields.ArrayField(models.CharField(max_length=200, blank=True))
    counts = fields.ArrayField(models.IntegerField())
    count_in_files = JSONField(default="")
