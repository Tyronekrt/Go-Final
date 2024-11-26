import json

import requests
from apt.package import Record
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests.auth import HTTPBasicAuth

from myapp.credentials import MpesaAccessToken, LipanaMpesaPpassword
from myapp.models import Appointment, Contact, User, ImageModel
from myapp.forms import AppointmentForm, ImageUploadForm


# Create your views here.
def index(request):
    if request.method == 'POST':
        if User.objects.filter(
            username=request.POST['username'],
            password=request.POST['password']
        ).exists():
            return render(request, 'index.html')
        else:
            return render(request,'login.html')
    else:
        return render(request, 'login.html')
def service(request):
    return render(request,'service-details.html')

def starter(request):
    return render(request,'starter-page.html')
def about(request):
    return render(request,'about.html')
def doctors(request):
    return render(request, 'doctors.html')
def myservice(request):
    return render(request, 'services.html')
def appointment(request):
    if request.method == 'POST':
       myappointments = Appointment(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            date=request.POST['date'],
            department=request.POST['department'],
            doctor=request.POST['doctor'],
            message=request.POST['message'],
        )
       myappointments.save()
       return redirect('/appointment')
    else:
        return render(request,'appointment.html')

def show(request):
    allappointments = Appointment.objects.all()
    return render(request, 'show.html',{'appointment':allappointments})

def delete(request, id):
    appoint=Appointment.objects.get(id=id)
    appoint.delete()
    return redirect('/show')

def contact(request):
    if request.method == 'POST':
        contacts=Contact(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message'],
        )
        contacts.save()
        return redirect('/contact')
    else:
        return render(request, 'contact.html')

def records(request):
    allcontacts = Contact.objects.all()
    return render(request, 'records.html',{'contact':allcontacts})

def deliting(request, id):
    # Fetch the contact record to delete
    contact = Contact.objects.get(id=id)
    contact.delete()
    return redirect('/records')

def edit(request,id):

    editappointment=Appointment.objects.get(id = id)

    return render(request,'edit.html',{'appointment':editappointment})

# def update(request,id):
#     updateinfo=Appointment.objects.get
#     form=AppointmentForm(request.POST,instance=updateinfo)
#     if form.is_valid():
#         form.save()
#         return redirect('/show')
#     else:
#         return render(request,'edit.html')

def update(request, id):
    updateinfo = Appointment.objects.get(id=id)  # Fetch the specific appointment object
    if request.method == 'POST':  # Handle POST requests only
        form = AppointmentForm(request.POST, instance=updateinfo)  # Bind form to the instance
        if form.is_valid():  # Validate the form
            form.save()  # Save the updated data
            return redirect('/show')  # Redirect to the show page
        else:
            return render(request, 'edit.html', {'appointment': updateinfo, 'errors': form.errors})
    else:
        return render(request, 'edit.html', {'appointment': updateinfo})  # Render the edit form if not POST

def register(request):
    # return render(request,'register.html')
    if request.method == 'POST':
        members = User(
            name=request.POST['name'],
            username=request.POST['username'],
            password=request.POST['password']
        )
        members.save()
        return redirect('/login')
    else:
        return render(request, 'register.html')
def login(request):
    return render(request,'login.html')

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/showimage')
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})

def show_image(request):
    images = ImageModel.objects.all()
    return render(request, 'show_image.html', {'images': images})

#Mpesa API views
def token(request):
    consumer_key = 'OtCn9VBqNTaciSrEHBsuAu2EevmC8BBzUF2oxMSvUvVtRrHr'
    consumer_secret = 'jiYeRp9wHxZJI0VA3hwt3Dx6WXnEzg2h448Lljlcd6UKO4pFVwz7cCmr9z38lay7'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')



def stk(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Payment made successfully!!")
