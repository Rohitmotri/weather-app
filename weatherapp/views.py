import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import Cityform

def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=3b5e60b72736f7fb718dc1bf086c4d1c'

    err_msg = ''
    message =''
    message_class = ''

    if request.method == 'POST':
        form = Cityform(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name = new_city).count()
       
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save()
                else:
                    err_msg='are you sure that you are from earth!'
            else:
                err_msg = 'city already exist you asshole'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'city added successfully'
            message_class = 'is-success'
            
    print(err_msg)

    form = Cityform()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data,
         'form' : form,
         'message':message,
         'message_class':message_class
         }
    return render(request, 'weatherapp/main.html', context)

def delete(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('weather')