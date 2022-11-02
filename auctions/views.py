from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


from django.views.generic.edit import FormView
from .forms import HackForm
from .models import Hack
class HackFormView(FormView):
    template_name = 'auctions/hacks.html'
    form_class = HackForm
    success_url = '/'

    def form_valid(self, form):
        print(self)
        print(self.request)
        print(self.request.user)
        if self.request.user.is_authenticated:
            h,_ = Hack.objects.get_or_create(user=self.request.user)
            h.listing_count = max(0, h.listing_count+form.cleaned_data["listings"])
            h.watchlist_count = max(0, h.watchlist_count+int(form.cleaned_data["watchlist"]))
            h.save()
        return super().form_valid(form)

from django.http import JsonResponse
def api_get_counters(request):
    if request.user.is_authenticated:
        h,_ = Hack.objects.get_or_create(user=request.user)
        result = {
            'my_watchlist_count': h.watchlist_count,
            'my_listings_count': h.listing_count,
            'all_listings_count': sum([h.listing_count for h in Hack.objects.all()])
        }
    else:
        result = {
            'my_watchlist_count': 0,
            'my_listings_count': 0,
            'all_listings_count': sum([h.listing_count for h in Hack.objects.all()])
        }
    print(f'api_get_counters returning {result}')
    return JsonResponse(result)