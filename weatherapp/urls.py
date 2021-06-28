from django.urls import path,include
from . import views

urlpatterns=[
	path('',views.weather,name='weather'),
	path('delete/<city_name>/',views.delete,name ='delete_city')
]