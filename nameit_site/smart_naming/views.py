from django.http import HttpResponse
from django.shortcuts import render
from .models import RepoWordCountView


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def word_profile(request, word):
    word_records = RepoWordCountView.objects.select_related('repo').filter(word=word)
    context = {"records": word_records, "word": word}
    return render(request, 'word_profile.html', context)
