from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import tutorial, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm

# Create your views here.

def single_slug(request, single_slug):
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        matching_series=TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)

        series_urls = {}
        for m in matching_series.all():
            part_one = tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published")
            series_urls[m] = part_one.tutorial_slug
        return render(request,
                      "main/category.html",
                      {"part_ones": series_urls})

    tutorials = [t.tutorial_slug for t in tutorial.objects.all()]
    if single_slug in tutorials:
        this_tutorial = tutorial.objects.get(tutorial_slug = single_slug)
        tutorials_from_series = tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_published")
        this_tutorial_index = list(tutorials_from_series).index(this_tutorial)
        return render(request,
                      "main/tutorial.html",
                      {"tutorial":this_tutorial,
                      "sidebar": tutorials_from_series,
                      "this_tutorial_index": this_tutorial_index})

    return HttpResponse(f"{single_slug} does not corespond to anything")

def homepage(request):
    return render(request=request,
                  template_name="main/categories.html",
                  context={"categories": TutorialCategory.objects.all})
def register(request):
    if request.method =="POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Acc Created: {username}")
            login(request, user)
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
                print(form.error_messages[msg])


    form = NewUserForm
    return render(request,
                  "main/register.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "logged out")
    return redirect("main:homepage")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"Successfull logged in as {username}")
            return redirect("main:homepage")
        else:
            messages.error(request, "STH is WRONG")
    form = AuthenticationForm
    return render(request,
                  "main/login.html",
                  {"form":form})
