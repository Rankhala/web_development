from django.db import models

# Create your models here.
#Airport model
class Airport(models.Model):
	city = models.CharField(max_length=64)
	code = models.CharField(max_length=3)

	def __str__(self):
		return f"{self.city} ({self.code})"

#flight model
class Flight(models.Model):
	origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
	destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
	duration = models.IntegerField()

	def __str__(self):
		return f"{self.id}: {self.origin} to {self.destination}"

#Passenger model
class Passenger(models.Model):
	name = models.CharField(max_length=64)
	surname = models.CharField(max_length=64)
	flights = models.ManyToManyField(Flight, blank=True, related_name="passenger")

	def __str__(self):
		return f"{self.name} {self.surname}"