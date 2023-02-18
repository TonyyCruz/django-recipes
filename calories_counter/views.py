from django.shortcuts import render


def home(request):
    return render(request, "calories_counter/pages/home.html")
