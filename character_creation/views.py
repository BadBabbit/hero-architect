from django.shortcuts import render
from django.http import HttpResponse


def create_character(request):
    context = {}
    return render(request, 'TODO.html', context)

def my_characters(request):
    context = {}
    return render(request, 'TODO.html', context)

def character_detail(request):
    context = {}
    return render(request, 'TODO.html', context)

def main():
    pass


if __name__ == "__main__":
    main()

