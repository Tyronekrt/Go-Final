from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('service/', views.service, name='service'),
    path('starter/', views.starter, name='starter'),
    path('about/', views.about, name='about'),
    path('doctors/', views.doctors, name='doctors'),
    path('myservice/', views.myservice, name='myservice'),
    path('appointment/', views.appointment, name='appointment'),
    path('show/', views.show, name='show'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('contact/', views.contact, name='contact'),
    path('records/', views.records, name='records'),
    path('deliting/<int:id>/', views.deliting, name='delete_record'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('update/<int:id>/', views.update, name='update'),
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('uploadimage/', views.upload_image, name='upload'),
    path('showimage/', views.show_image, name='image'),

#Mpesa API urls
    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),

]
