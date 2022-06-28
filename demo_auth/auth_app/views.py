import requests, json
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from .forms import AuthForm

from django.contrib.auth import authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
CIVILID_AUTH_URL = ""


def base_form(request):
    # This is the view where the form is rendered and served.
    context = {}
    context["form"] = AuthForm
    return render(request, "civ_form.html", context=context)


def land_form(request):
    """This is the view where form is submitted."""
    flag = True
    if request.method == "POST":
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            cleaned_data = auth_form.cleaned_data
            civ_id = cleaned_data["civ_id"]

            # Set CIVILID_AUTH_URL in settings.py(base.py) without the endpoints
            url = CIVILID_AUTH_URL + "InitiateAuthRequestPN/"
            callback_url = "example.com"
            req = requests.post(
                url, json={"personCivilNo": civ_id, "spCallbackURL": callback_url}
            )

            # Set key, value
            cache_key = "authed"
            cache_value = False
            # Establish key-value in cache.
            if cache.get(cache_key) is None:
                cache.set(cache_key, cache_value, 300)
            # Enable a spinner here.
            return render(request, "civ_form.html")
    else:
        return render("500.html")


def is_authed(request):
    """This view is the polling point for the
    frontend to check if auth status is complete."""

    refr = {"refresh": False}
    # Case where civ_key has been auth'd successfully

    if cache.get("authed") == "False" or cache.get("authed") == False:
        refr["refresh"] = False
        return JsonResponse(refr)
    else:
        # Authenticate the civil id.
        civ_id = cache.get("auth_id")
        authenticate(civil_id=civ_id)
        # Clear cache keys.
        cache.delete("authed")
        cache.delete("auth_id")
        return JsonResponse(refr)


@csrf_exempt
def inter_state(request):
    """This view is the endpoint of callback uri."""

    # Set cache key according to status codes.
    if request.method == "POST":
        # result_codes = {
        #     "1": JsonResponse({"status": "ok"}),
        #     "2": JsonResponse({"status": "Cert Revoked"}),
        #     "3": JsonResponse({"status": "Failed To Verify"}),
        #     "4": JsonResponse({"status": "Decline"}),
        #     "5": JsonResponse({"status": "Expired"}),
        # }
        json_data = json.loads(request.body)
        result_code = json_data["MIDAuthSignResponse"]["ResultDetails"]["ResultCode"]
        civ_id = json_data["MIDAuthSignResponse"]["ResultDetails"]["UserCivilNo"]
        if result_code.startswith("1"):
            cache.set("authed", True, 300)
            cache.set("auth_id", civ_id, 300)

    return render(request, "interm.html")