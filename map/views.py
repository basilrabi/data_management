from django.shortcuts import render

def index(request):
    return render(request, 'map/index.html', {})

def road(request):
    return render(request, 'map/road.html', {})
