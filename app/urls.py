from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("", views.index, name= "home"),
    path("register", views.register, name= "register"),
    path("vendor_register", views.vendor_register, name= "vendor_register"),
    path("log_in", views.log_in, name= "log_in"),
    path("vendor_log_in", views.vendor_log_in, name= "vendor_log_in"),
    path("dashboard", views.dashboard, name= "dashboard"),
    path("e_market", views.e_market, name= "e_market"),
    path('upload_crop_image/', views.upload_crop_image, name='upload_crop_image'),
    path("log_out", views.log_out, name= "log_out"),
    path('vendor_dashboard', views.vendor_dashboard, name='vendor_dashboard'),
    path("crop_report", views.crop_report, name= "crop_report"),
    path("report", views.report, name= "report"),
    path("add_to_cart/<int:item_id>/", views.add_to_cart, name= "add_to_cart"),
    path("report1", views.report1, name= "report1"),
    path("news", views.news, name= "news"),
    path("loan1", views.loan1, name= "loan1"),
    path("insurance", views.insurance, name= "insurance"),
    path("crop_prediction", views.crop_prediction, name= "crop_prediction"),
    path("crop_dis", views.crop_dis, name= "crop_dis"),
    path("fert_rec", views.fert_rec, name= "fert_rec"),
    path("fert_report", views.fert_report, name= "fert_report"),
    path('upload',views.upload , name='upload'),
    path('predict',views.predict , name='predict'),
    path('search_news/', views.search_news, name='search_news'),

]