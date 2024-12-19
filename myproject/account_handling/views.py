from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username= username, password = password)

        errors = {}

        if user is not None:
            auth.login(request, user)
            return redirect('homepage')
        else:
            errors['invalid'] = ("Invalid Credintials")
            return render(request, 'app_one/login.html', {'errors': errors})
        
    return render(request, 'account_handling/login.html')

def signup(request):
    if request.method == 'POST':
        error = {}
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_pass = request.POST.get('conf_pass')
        
        errors = validate_signup(username, email, password, conf_pass)

        if not errors:
            request.session['username'] = username
            request.session['email'] = email 
            request.session['password'] = password
            return render(request, 'app_one/signup.html', {'show_modal': True})
        else:
            return render(request, 'app_one/signup.html', {'errors': errors})

    
    return render(request, 'account_handling/signup.html')

def validate_signup(username, email, password, conf_pass):
    errors = {}

    if password != conf_pass:
        errors['password'] =("Passwords do not match")

    if User.objects.filter(email=email).exists():
        errors['email'] =("Email already in use")
        
    if User.objects.filter(username=username):
        errors['username'] =("Username already exists")

    has_caps = any(char.isupper() for char in password)
    has_digits = any(char in "1234567890" for char in password)
    has_special = any(char in "~`!@#$%^&*()-_+={}[]|\\;:<>,./?" for char in password)


    if len(password) <= 8 or not has_caps or not has_digits or not has_special:
        errors['password_requirments'] = (
                "Password must be at least 8 characters long and include at least 1 uppercase letter, 1 number, and 1 special character " + "~`!@#$%^&*()-_+={}[]|\\;:<>,./?"
            )
    return errors
