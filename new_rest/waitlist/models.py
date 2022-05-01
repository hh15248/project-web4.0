from django.db import models
import time
from datetime import datetime
from django.utils import timezone

# Create your models here.
tz = timezone.get_default_timezone()

# Waitlist
class Wait(models.Model):
    # Guest name
    name = models.CharField(max_length = 120, unique=True) 
    # Size of Party
    party_size = models.CharField(max_length = 20)
    # Time of Arrival
    arrival_time = models.DateTimeField(auto_now_add = True)
    # Assignment suggestion
    assign_sugg = models.IntegerField(default=0)

    @property
    def wait_time(self):
        current_time = datetime.now(tz)
        wait_time = current_time - self.arrival_time
        return wait_time.total_seconds() // 60

    def __str__(self):
        return self.name

# Tables
class Table(models.Model):
    # Table number
    number = models.IntegerField(unique=True)
    # Party name
    party = models.CharField(max_length = 20, default = "Empty")
    # Seating capacity of table
    seats = models.IntegerField()
    # Time seated
    time_seated = models.DateTimeField(auto_now_add = True)
    # Server
    server = models.CharField(max_length = 20, default = "None")

    @property
    def dining_time(self):
        current_time = datetime.now(tz)
        dining_time = current_time - self.time_seated
        return dining_time.total_seconds() // 60

    def __str__(self):
        name = "Table " + str(self.number)
        return name

class Config(models.Model):
    # Number of Servers
    number_of_servers = models.IntegerField(default = 0)
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
