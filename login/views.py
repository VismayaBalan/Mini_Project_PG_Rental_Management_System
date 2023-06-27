from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Pglist,User,Customer
# Create your views here.

@login_required(login_url = 'login')
def index(request):
    return render(request, "home.html")


def home_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    pgList = Pglist.objects.all()
    print(Pglist.objects.all())
    context={
        'pgList': pgList
    }
    return render(request, "home.html",context)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username,password)
        user = authenticate(request,username = username, password = password)
        print(user)
        if user is not None:
            login(request,user)
            return render(request, "home.html")
        else:
            return render(request, "login.html",{
                "error" : "Invalid Credentials"
            })
        
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return render(request,"login.html",{
        "error":"Logged Out..!!"
    })


def csignup(request):
    if request.method == "POST":
        Username = request.POST["username"]
        Email = request.POST["email"]
        Password = request.POST["password"]
        cPassword = request.POST["cpassword"]
        pref_location = request.POST["preferedlocation"]
        Description = request.POST["description"]

        if Password != cPassword :
            return render(request,"csignup", {
                "error":"Passwords does not match"
            })
        
        if pref_location != " " and Description != " ":
            try:
                user = User.objects.create_user(Username,Email,Password)
                user.role = 'owner'
                user.save()

                owner = Customer.objects.create(uuser = user,plocation = pref_location,description = Description)
                owner.save()

            except IntegrityError:
                return render(request,"csignup.html",{
                    "error": "User already Exists"
                })
            
            login(request,user)
            return render (request, 'home_owner.html')

        else:
            try:
                user = User.objects.create_user(Username,Email,Password)
                user.role = 'customer'
                user.save()

                customer = Customer.objects.create(uuser = user)
                customer.save()

            except IntegrityError:
                return render(request,"csignup.html",{
                    "error": "User already Exists"
                })
            
            login(request,user)
            return render (request, 'home.html')

    else:
        return render(request, 'csignup.html')

        

