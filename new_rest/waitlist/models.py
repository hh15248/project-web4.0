from re import L
from django.db import models
import time
from datetime import datetime
from django.utils import timezone


# Create your models here.
tz = timezone.get_default_timezone()

# Tables
class Table(models.Model):
    # Table number
    number = models.IntegerField(unique=True)
    # Party name
    party = models.CharField(max_length = 20, default = "Empty")
    # Seating capacity of table
    seats = models.IntegerField()
    # Party Size
    party_size = models.IntegerField()
    # Time seated
    time_seated = models.DateTimeField(auto_now_add = True)
    # Server
    server = models.CharField(max_length = 20, default = "None")

    @property
    def dining_time(self):
        if self.party in ["Empty","Pending"]:
            return 0
        current_time = datetime.now(tz)
        dining_time = current_time - self.time_seated
        return dining_time.total_seconds() // 60

    def __str__(self):
        name = "Table " + str(self.number)
        return name

# Waitlist
class Wait(models.Model):
    # Guest name
    name = models.CharField(max_length = 120, unique = True)
    # Size of Party
    party_size = models.CharField(max_length = 20)
    # Time of Arrival
    arrival_time = models.DateTimeField(auto_now_add = True)
    # Assignment suggestion
    assign_sugg = models.IntegerField(default = 0)
    # Etimated wait time
    est_wait = models.IntegerField(default = 0)

    @property
    def wait_time(self):
        current_time = datetime.now(tz)
        wait_time = current_time - self.arrival_time
        return wait_time.total_seconds() // 60


    def __str__(self):
        return self.name

class Config(models.Model):
    # Server Names
    server_names = models.CharField(max_length = 50, default = "None")
    # Tables of 2
    tables_for_2 = models.IntegerField(default = 0)
    # Tables of 4
    tables_for_4 = models.IntegerField(default = 0)
    # Tables of 6
    tables_for_6 = models.IntegerField(default = 0)
    # Tables of 8
    tables_for_8 = models.IntegerField(default = 0)

    def __str__(self):
        name = "Configuration for " + str(self.server_names)
        return name

class WaitlistHistory(models.Model):
    # Guest name
    name = models.CharField(max_length = 120)
    # Size of Party
    party_size = models.CharField(max_length = 20)
    # Arrival time
    arrival_time = models.DateTimeField(auto_now_add = True)
    # Wait time
    wait_time = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

class TableHistory(models.Model):
    # Party name
    party = models.CharField(max_length = 20, default = "Empty")
    # Party Size
    party_size = models.IntegerField()
    # Server
    server = models.CharField(max_length = 20, default = "None")
    # Time Seated
    time_seated = models.DateTimeField(auto_now_add = True)
    # Dining time
    dining_time = models.CharField(max_length = 20)

    def __str__(self):
        return self.party
