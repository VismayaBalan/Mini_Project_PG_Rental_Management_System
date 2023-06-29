from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
from .models import Pglist,User,Customer
# Create your views here.

@login_required(login_url = 'login')
def index(request):
    # return render(request, "home.html")
    pgList = Pglist.objects.all()
    print("------->",pgList)
    return render(request, "home.html", {
        'pgList' : pgList
    })


def home_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    pgList = Pglist.objects.filter(booking_status="Not Booked")
    context = {
        'pgList': pgList
    }
    return render(request, "home.html", context)



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect("home")
        else:
            return render(request, "login.html",{
                "error" : "Invalid Credentials"
            })
        
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return render(request,"login.html")


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
            return render (request, 'login.html')

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
            return render (request, 'login.html')

    else:
        return render(request, 'csignup.html')

        
@login_required(login_url='login')
def addPg(request):
    user = request.user
    if request.method == "POST" and user.role == "owner":
        Pname = request.POST["name"]
        Email = request.POST["email"]
        Phoneno = request.POST["phoneno"]
        Address = request.POST["address"]
        Image = request.FILES["images"]
        Createdby = user.username

        pg = Pglist.objects.create( name=Pname,email=Email,phoneNumber=Phoneno,address=Address,image=Image,createdby=Createdby )
        pg.save()

        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request,"addpg.html")
    

@login_required(login_url='login')
def deletePg(request, pg_id):
    user = request.user
    
    if user.role == 'owner':
        try:
            pg_id = int(pg_id)
            pg = Pglist.objects.get(id=pg_id, createdby=user.username)
            pg.delete()
            return HttpResponseRedirect(reverse('home')) 
        except Pglist.DoesNotExist:
            return HttpResponseRedirect(reverse("home"))
        

@login_required(login_url='login')
def myPg(request):
    user = request.user
    pgList = Pglist.objects.filter(createdby = user.username)
    return render(request, "mypg.html", {
        'pgList' : pgList
    })

def searchPg(request):
    query = request.POST["query"]
    if query:
        pglist = Pglist.objects.filter(name__icontains=query)  
    else:
        pglist = Pglist.objects.none()  
    
    context = {
        'pglist': pglist,
        'query': query,
    }
    return render(request, 'searchpg.html', context)

@login_required(login_url='login')
def bookPg(request, pg_id):
    user = request.user
    
    if user.role == 'customer':
        try:
            pg_id = int(pg_id)
            pg = Pglist.objects.get(id=pg_id)
            if pg.booking_status != Pglist.BOOKED:  
                pg.booking_status = Pglist.BOOKED
                pg.booked_by = user.username
                pg.save()
            return HttpResponseRedirect(reverse('home')) 
        except Pglist.DoesNotExist:
            return HttpResponseRedirect(reverse("home"))
        
@login_required(login_url='login')
def updateBookPg(request, pg_id):
    user = request.user
    
    if user.role == 'owner':
        try:
            pg_id = int(pg_id)
            pg = Pglist.objects.get(id=pg_id)
            if pg.booking_status == Pglist.BOOKED:  
                pg.booking_status = Pglist.NOT_BOOKED
                pg.booked_by = " "
                pg.save()
            return HttpResponseRedirect(reverse('mypg')) 
        except Pglist.DoesNotExist:
            return HttpResponseRedirect(reverse("mypg"))
        

@login_required(login_url='login')
def customerBookPg(request):
    user = request.user
    
    if user.role == 'customer':
        pgList = Pglist.objects.filter( booked_by = user.username)
        context = {
        'pgList': pgList
    }
    return render(request, "customerbookpg.html", context) 
    
            
               
            
        
              

    