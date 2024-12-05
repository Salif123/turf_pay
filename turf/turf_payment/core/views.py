from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from .models import *

# Create your views here.
def home_view(request):
    return render(request,"home.html",context={})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home_view')  # Change 'home' to the name of your home page URL pattern
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_view')  # Change 'home' to the name of your home page URL pattern
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home_view')  # Change 'home' to the name of your home page URL pattern


def book_page(request):
    context = {}
    context["stadiums"] = Stadium.objects.all()
    print(Stadium.objects.all())
    return render(request, 'booknow.html',context)

def create_appointment(request):
    if request.method == 'POST':
        stadium_id = request.POST['stadium']
        time_slot = request.POST['time_slot']
        phone = request.POST['phone']

        stadium = Stadium.objects.get(id=stadium_id)
        user = request.user
        if stadium.booked == False:
            Appointment.objects.create(
                user=user,
                stadium=stadium,
                time_slot=time_slot,
                phone=phone
            )
            stadium.booked = True
            stadium.save()
            return HttpResponse("Success")
        else:
            return HttpResponse("Stadium is aldready booked")
    
@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'my_appointments.html', {'appointments': appointments})  

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    stadium = appointment.stadium
    appointment.delete()
    stadium.booked = False
    stadium.save()
    return HttpResponse("Appointment Deleted")

def items(request):
    return render(request, 'items.html')

from django.shortcuts import render

# Create your views here.
import razorpay

from django.conf import settings

def items(request):
    """Render the items list with total amount input."""
    return render(request, 'items.html')

def initiate_payment(request):
    """Create Razorpay order and send details to payment template."""
    if request.method == "POST":
        # Fetch amount from form in rupees
        amount = int(request.POST.get("amount", 0)) * 100  # Convert ₹ to paise
        
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Create an order
        payment = client.order.create({
            "amount": amount, 
            "currency": "INR", 
            "payment_capture": 1
        })
        
        # Send payment details to the template
        context = {
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "order_id": payment["id"],
            "amount": amount // 100  # Convert back to ₹
        }
        return render(request, 'payment2.html', context)
    

    return render(request, 'items.html')

def payment_success(request):
    """Handle payment success (optional redirect or save data)."""
    return render(request, 'payment_success.html')