from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from users.forms import LoginForms, RegistrationForms


def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()

            # Check if user exists and password is correct regardless of is_active
            try:
                user_obj = User.objects.get(username=username)
                if user_obj.check_password(password):
                    if not user_obj.is_active:
                        # Use AllowAllUsersModelBackend so Django restores
                        # the inactive user from session correctly
                        user_obj.backend = 'django.contrib.auth.backends.AllowAllUsersModelBackend'
                        auth.login(request, user_obj)
                        return redirect('banned')
                    else:
                        user = auth.authenticate(request, username=username, password=password)
                        auth.login(request, user)
                        messages.success(request, f'{username} logged in successfully!')
                        return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password.')
                    return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')

    return render(request, 'users/login.html', {'form': form})


def register(request):
    form = RegistrationForms()

    if request.method == 'POST':
        form = RegistrationForms(request.POST)

        if form.is_valid():
            if form['password1'].value() != form['password2'].value():
                messages.error(request, 'Passwords do not match.')
                return redirect('register')

            username = form['username'].value()
            email = form['email'].value()
            password = form['password1'].value()

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return redirect('register')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')

    return render(request, 'users/register.html', {'form': form})


def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


def banned(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_active:
        return redirect('home')
    return render(request, 'users/banned.html')




