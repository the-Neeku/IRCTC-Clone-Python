

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile 
from django.contrib.auth.decorators import login_required

# UserRegistrationForm 
class UserRegistrationForm(forms.Form): # Or forms.ModelForm for User/UserProfile
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    fullname = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))
    mobile = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Mobile Number', 'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if username and User.objects.filter(username=username).exists():
            self.add_error('username', "This username is already taken.")
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', "This email is already registered.")
        return cleaned_data

    def save(self):
        # This is a manual save, typically you'd use ModelForm
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        fullname = self.cleaned_data['fullname']
        mobile = self.cleaned_data['mobile']

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = fullname.split(' ')[0]
        user.last_name = ' '.join(fullname.split(' ')[1:]) if len(fullname.split(' ')) > 1 else ''
        user.save()
        

        return user


# UserLoginForm 
class login(forms.Form):
    username_or_email = forms.CharField(label="Username or Email",
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# NEW BookingForm

class BookingForm(forms.Form):
    """
    Form for ticket booking details.
    """
    # Choices for demonstration
    TRAIN_CLASSES = [
        ('1A', 'AC First Class (1A)'),
        ('2A', 'AC 2-Tier (2A)'),
        ('3A', 'AC 3-Tier (3A)'),
        ('SL', 'Sleeper (SL)'),
        ('2S', 'Second Seating (2S)'),
        ('CC', 'AC Chair Car (CC)'),
    ]

    QUOTAS = [
        ('GN', 'General'),
        ('CK', 'Tatkal'),
        ('LD', 'Ladies'),
        ('PT', 'Premium Tatkal'),
        # Add more quotas as needed
    ]

    from_station = forms.CharField(
        max_length=100,
        label="From Station",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., DELHI', 'class': 'form-control'})
    )
    to_station = forms.CharField(
        max_length=100,
        label="To Station",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., MUMBAI', 'class': 'form-control'})
    )
    journey_date = forms.DateField(
        label="Journey Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    train_class = forms.ChoiceField(
        choices=TRAIN_CLASSES,
        label="Train Class",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quota = forms.ChoiceField(
        choices=QUOTAS,
        label="Quota",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean_journey_date(self):
        journey_date = self.cleaned_data['journey_date']
        import datetime
        if journey_date < datetime.date.today():
            raise forms.ValidationError("Journey date cannot be in the past.")
        return journey_date
    from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
