from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name = "index"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("home", views.home_view, name = "home"),
    path("csignup",views.csignup,name="csignup"),
    path("addpg", views.addPg,name="addpg"),
    path("mypg", views.myPg,name="mypg"),
    path('searchpg', views.searchPg, name='searchpg'),
    path('deletepg/<str:pg_id>/', views.deletePg, name='deletepg'),
    path('bookpg/<str:pg_id>/', views.bookPg, name='bookpg'),
    path('updatebookpg/<str:pg_id>/', views.updateBookPg, name='updatebookpg'),
    path('customerbookpg', views.customerBookPg, name='customerbookpg'),
    path("", views.front, name = "front"),
    path("about", views.about, name = "about"),
    path("contact", views.contact, name = "contact")


 ]