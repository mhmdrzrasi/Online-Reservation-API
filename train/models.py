from django.db import models

from accounts.models import User


class Train(models.Model):
    train_number = models.CharField(max_length=8)
    coupe_number = models.CharField(max_length=8)
    features = models.CharField(max_length=256)
    capacity = models.IntegerField()

    # میتونست در یک کلاس دیگر تعریف شود ولی به علت کمبود وقت و همچنین انجام این نوع کلاس بندی در اپ هتل منصرف شدم
    image = models.ImageField(upload_to='images/')
    starting_city = models.CharField(max_length=128)
    destination_city = models.CharField(max_length=128)
    departure_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return self.train_number


class Invoice(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='invoices_train')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices_train')

    def __str__(self):
        return f"{self.train} - {self.passengers.count()} person"


class Passenger(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    national_id = models.CharField(max_length=10)
    birthday = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='passengers')

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
