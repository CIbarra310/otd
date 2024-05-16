from django.shortcuts import render

# - Home Page
def home(request):
    return render(request, 'interface/index.html')