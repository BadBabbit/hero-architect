from django.shortcuts import render

def home(request):
    context = {}
    if request.user.is_authenticated:
        context["username"] = request.user.username
    return render(request, 'home.html', context=context)