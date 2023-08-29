from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Flight, Airport, Passenger
from django.urls import reverse

# Create your views here.
def index(request):
	flights = Flight.objects.all()
	return render(request, "airline/index.html", {
			"flights": flights
		})

def flight(request, flight_id):
	flight = Flight.objects.get(id=flight_id)
	passengers = flight.passenger.all()
	non_passengers = Passenger.objects.exclude(flights=flight).all()
	return render(request, "airline/flight.html", {
			"flight": flight,
			"passengers": passengers,
			"non_passengers": non_passengers
		})

def book(request, flight_id):
	if request.method == "POST":
		flight = Flight.objects.get(pk=flight_id)

		#The actual value that will be submitted through the form is passenger id
		#Passenger is just a name used to access the form value
		passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
		passenger.flights.add(flight)

		#Redirect user to the flight page
		return HttpResponseRedirect(reverse("flight", args=(flight.id,)))