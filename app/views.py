from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse

from django.contrib.auth.decorators import login_required
import requests


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')


from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserForm, ProfileForm  # Assuming forms are defined in forms.py

def registration(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        pf = ProfileForm(request.POST, request.FILES)
        
        if uf.is_valid() and pf.is_valid():
            user = uf.save(commit=False)
            password = uf.cleaned_data['password']
            user.set_password(password)
            user.save()

            profile = pf.save(commit=False)
            profile.profile_user = user
            profile.save()

            send_mail(
                'Registration',
                'Thanks for registration, your registration is successful.',
                'suaraabinash1@gmail.com',
                [user.email],
                fail_silently=False
            )

            return HttpResponse('Registration is successful')

    else:
        uf = UserForm()
        pf = ProfileForm()

    return render(request, 'registration.html', {'uf': uf, 'pf': pf})




def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)

        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('u r not an authenticated user')
    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



@login_required
def search(request):
    if request.method=='POST':
        city_name=request.POST['city']
        api_key = '6960337269eb715dc8fdfee3fe8c6baf'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
        response = requests.get(url)
        weather_data = response.json()
        print(weather_data)
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather=weather_data['main']['feels_like']
        speed=weather_data['wind']['speed']
        username=request.session.get('username')
        LUO=User.objects.get(username=username)
        obj=WeatherData.objects.get_or_create(username=LUO,city=city_name, temperature=temperature, humidity=humidity,weather=weather, speed=speed)[0]
        obj.save()
        d={'obj':obj}
        return render(request,'search.html',d)
    
    return render(request,'search.html')



@login_required
def user_history(request):
    username=request.session['username']
    UO=User.objects.get(username=username)
    LWO=WeatherData.objects.filter(username=UO)

    d={'LWO':LWO}
    return render(request,'user_history.html',d)


def all_history(request):
    LWO=WeatherData.objects.all()
    d={'LWO':LWO}
    return render(request,'all_history.html',d)
