from django.shortcuts import render


def index(request):
    return render(request, 'cms/index.html', {})


def about(request):
    return render(request, 'cms/about.html', {})