from django.shortcuts import render


# Create your views here.
def main(request):
    return render(request, "app_instagram/index.html", context={"title": "Web 9 Group!"})
