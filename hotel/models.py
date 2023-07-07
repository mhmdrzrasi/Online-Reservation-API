from django.db import models

from accounts.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=512)
    city = models.CharField(max_length=128)
    stars = models.IntegerField()
    features = models.CharField(max_length=256)

    @property
    def capacity(self):
        return sum(room.number_of_rooms * room.beds for room in self.rooms.all())

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return ''
        # return self.image.url


class Room(models.Model):
    number_of_rooms = models.IntegerField()
    beds = models.PositiveSmallIntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')

    def __str__(self):
        return ''
        # return f"{self.number_of_rooms} * {self.beds}"


class Invoice(models.Model):
    entry_date = models.DateField()
    leave_date = models.DateField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='invoices')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')

    @property
    def beds(self):
        return self.passengers.count()

    def __str__(self):
        return f"{self.hotel} - {self.beds} person"


class Passenger(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    national_id = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=11)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='passengers')

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
