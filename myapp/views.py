
import requests
import json
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
from django.shortcuts import render,redirect
from myapp.credentials import MpesaAccessToken, LipanaMpesaPpassword
from myapp.models import Appointment, Member, ImageModel
from myapp.models import Contact
from myapp.forms import AppointmentForm, ImageUploadForm
# Create your views here.
def index(request):              #when redirected to login
    if request.method == 'POST': #get to username and password to check if they exist
        if Member.objects.filter(
                username=request.POST['username'],
                password=request.POST['password'],
        ).exists():             #after confirming they exist by fetching
            members = Member.objects.get(
                username=request.POST['username'],
                password=request.POST['password'],
            )
            return render(request, 'index.html', {'members': members})

        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def services(request):
    return render(request, 'service-details.html')

def starter(request):
    return render(request, 'starter-page.html')

def about(request):
    return render(request, 'about.html')

def myservice(request):
    return render(request, 'services.html')

def doctors(request):
    return render(request, 'doctors.html')

def appointment(request):
    if request.method == "POST":
        myappointment=Appointment(
                    name=request.POST['name'],
                    email=request.POST['email'],
                    phone=request.POST['phone'],
                    date=request.POST['date'],
                    department=request.POST['department'],
                    doctor=request.POST['doctor'],
                    message=request.POST['message'],
        )
        myappointment.save()
        return redirect('/show') # Redirect to show after saving. Show is the page that displays the appointment data. It inherits from starter.html

    else:
        return render(request, 'appointment.html') #same template


def contact(request):
    if request.method == "POST":
        mycontact = Contact(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message']
        )
        mycontact.save()
        return redirect('/contactshow')  # Redirect after saving

    return render(request, 'contact.html') #same template

def show(request): #Render file show.html, despite rendering, it should also show the values in allappointments
    allappointments = Appointment.objects.all() #All models in Appointment saved in var allappointments
    return render(request, 'show.html',{'appointment':allappointments}) #key can be any name ie firstname /'appointment'. Used to mention anything in variable allappointments


#Delete function and assign the values for Appointment
# fetch specific records and store in variable appoint

def delete(request,id):
    appoint=Appointment.objects.get(id=id)
    appoint.delete()
    return redirect('/show')

def contactshow(request):
    allcontacts = Contact.objects.all() # Fetch all contacts from the database
    return render(request, 'contactshow.html', {'contacts':allcontacts}) # Pass data to the template

def delete(request,id):
    contact=Contact.objects.get(id=id)
    contact.delete()
    return redirect('/contactshow')

# EDITING Appointment DETAILS
def edit(request,id):
    editappointment=Appointment.objects.get(id=id) #When edit button is hit, it gets appointment details and stores them in editappointment as the key
    return render(request, 'edit.html',{'appointment':editappointment})
#Change existing data
def update(request,id):
    updateinfo = Appointment.objects.get(id=id) #call update, fetches appointment details and stores them in var
    form = AppointmentForm(request.POST, instance=updateinfo)  #whatever is updated is stored in var form
    if form.is_valid():  #to validate values sent to appointment form if are valid
        form.save()
        return redirect('/show')
    else:
        return render(request, 'edit.html')

#Register and login
def register(request):
    if request.method == "POST":
        members=Member(
            name=request.POST['name'], #green name is from the form while red from models.py
            username=request.POST['username'],
            password=request.POST['password']
        )
        members.save()       #When we save, we want to be redirected to login form
        return redirect('/login')

    else:
        return render(request, 'register.html')





def login(request):
    return render(request, 'login.html')


#upload, show,delete
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

def imagedelete(request, id):
    image = ImageModel.objects.get(id=id)
    image.delete()
    return redirect('/showimage')

#payment
def token(request):
    consumer_key = 'QvN33HKxfsA3QdgoGJPVNqVq6fe9f9xOviq64JyYDVY4b5Jo'
    consumer_secret = 'FgDlbXWa0tYUnJBifnjzxZralue0RGzqDwzAlOMha1F28XBgLC5ZasSVDjww9Wl6'
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
        return HttpResponse("Success")

