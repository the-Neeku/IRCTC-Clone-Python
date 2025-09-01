# myproject/myapp/views.py
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from .models import Booking
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout 
from reportlab.pdfgen import canvas

def home(request):
   
    return render(request, 'index.html')


def contact(request):
   
    return render(request, 'contact.html')



def registration(request):
    if request.method == 'POST':
        Username = request.POST['username']
        Fullname = request.POST['fullname']
        Email = request.POST['email']
        Password = request.POST['password']
        Mobile = request.POST['mobile']

        if User.objects.filter(username=Username).exists():
            messages.error(request, "Username already exists")
            return redirect('registration')

        user = User.objects.create_user(username=Username, email=Email, password=Password)
        user.save()

        # send emil on successful registration
        send_mail(
            subject='Welcome to IRCTC!',
            message=f"Hi {Fullname}, your account has been created successfully!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[Email],
            fail_silently=False,
        )

        messages.success(request, "Account created successfully. Check your email.")
        return redirect('login')

    return render(request, 'registration.html')


# change function name
def user_login(request): 
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            try:
                user_by_email = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_by_email.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('UserProfile')  
        else:
            messages.error(request, "Invalid credentials.")
            return render(request, 'login.html', {'username_or_email': username_or_email})
    
    return render(request, 'login.html')

    
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')  


# Placeholder views for the form actions on index.html
@login_required
def pnr_status_view(request):
    return render(request, 'pnr_status.html') # Consistent path



@login_required
def UserProfile(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'UserProfile.html', {'bookings': bookings})




@login_required
def ticket_booking(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        from_station = request.POST.get('from_station')
        to_station = request.POST.get('to_station')
        date = request.POST.get('date')
        seats = request.POST.get('seats')

        pnr = get_random_string(length=10).upper()

        # Save booking
        Booking.objects.create(
            user=request.user,
            pnr=pnr,
            name=name,
            email=email,
            from_station=from_station,
            to_station=to_station,
            journey_date=date,
            seats=seats
        )

        # Send email
        message = f"""
        Dear {name},

        Your ticket has been booked successfully!

        🚆 From: {from_station}
        🛤️ To: {to_station}
        📅 Date: {date}
        🎟️ Seats: {seats}
        🆔 PNR: {pnr}

        Thank you for choosing IRCTC.
        """
        send_mail(
            subject='IRCTC Ticket Confirmation',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        # messages.success(request, "Ticket booked and confirmation email sent!")
        return redirect('UserProfile')

    return render(request, 'ticket_booking.html')

@login_required
def search_tickets(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            from_station = form.cleaned_data['from_station']
            to_station = form.cleaned_data['to_station']
            journey_date = form.cleaned_data['journey_date']
            train_class = form.cleaned_data['train_class']
            quota = form.cleaned_data['quota']
            


            messages.success(request, "Search successful!")
            return render(request, 'search_tickets.html', {
                'from_station': from_station,
                'to_station': to_station,
                'journey_date': journey_date,
                'train_class': train_class,
                'quota': quota,
            })
        else:
            messages.error(request, "Form is invalid.")
            return render(request, 'search_tickets.html', {'form': form})
    else:
        form = BookingForm()
        return render(request, 'search_tickets.html', {'form': form})




@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required
def download_ticket_pdf(request, pnr):
    booking = Booking.objects.get(pnr=pnr, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=IRCTC_Ticket_{pnr}.pdf'

    p = canvas.Canvas(response)
    p.setTitle(f"IRCTC Ticket {pnr}")

    p.drawString(100, 800, "IRCTC Railway Ticket")
    p.drawString(100, 780, f"PNR: {booking.pnr}")
    p.drawString(100, 760, f"Name: {booking.name}")
    p.drawString(100, 740, f"Email: {booking.email}")
    p.drawString(100, 720, f"From: {booking.from_station}")
    p.drawString(100, 700, f"To: {booking.to_station}")
    p.drawString(100, 680, f"Journey Date: {booking.journey_date}")
    p.drawString(100, 660, f"Seats: {booking.seats}")
    p.drawString(100, 640, f"Booking Time: {booking.booked_at.strftime('%d-%m-%Y %H:%M')}")

    p.showPage()
    p.save()

    return response

