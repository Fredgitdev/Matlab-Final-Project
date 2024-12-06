from django.db import models

# Create your models here.

class Student(models.Model):
    fullname = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    age = models.IntegerField()
    yob = models.DateField()

# saving using usernames
    def __str__(self):
        return self.fullname

#a new model

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    quantity = models.IntegerField()

#TO RETURN A NAME FOR THE DATA SAVED
    def __str__(self):
        return self.name

class Patient(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    dateofbirth = models.DateField()
    gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    email = models.EmailField()
    phonenumber = models.CharField(max_length=20)
    address = models.TextField(max_length=200)

    def __str__(self):
        return self.firstname + ' ' + self.lastname


class Appointment(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateTimeField()
    department = models.CharField(max_length=200)
    doctor = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.subject}"


#class for storing registration values (name, username and password)
class Member(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name  #after, ensure you makemigrations and migrate then get to admin.py  to import, Member then admin.site.register(Member)

#model to store an image, title and price
class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=50)
    price = models.CharField(max_length=50)

    def __str__(self):
        return self.title