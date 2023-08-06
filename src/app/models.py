from django.db import models
from django.contrib.auth.models import User
from random import randrange
from datetime import timedelta
from datetime import datetime
from random import randrange

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

d1 = datetime.strptime('2022-01-01', '%Y-%m-%d')
d2 = datetime.strptime('2023-01-01', '%Y-%m-%d')
rand_date = random_date(d1,d2)

status_choices = [('In Progress', 'In Progress'),('Completed', 'Completed')]
intake_choices = [('Web', 'Web'),('Email', 'Email'),('Phone','Phone')]
class Ticket(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    account_number = models.CharField(max_length=100, null=True, blank=True, default='#')
    updated_at = models.DateTimeField(auto_now=True)
    product = models.CharField(max_length=100, null=True, blank=True)
    agent_id = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='admin')
    complaint_date = models.DateField(default=rand_date)
    complaint_detail = models.TextField(null=True, blank=True)
    incident_category = models.CharField(max_length=100, null=True, blank=True, default='#')
    incident_subcategory = models.CharField(max_length=100, null=True, blank=True, default='#')
    customer_zip = models.CharField(max_length=100, null=True, blank=True, default='#')
    customer_state = models.CharField(max_length=50, null=True, blank=True, default='#')
    status = models.CharField(max_length=100, choices=status_choices, default="In Progress")
    intake_channel = models.CharField(max_length=100, choices=intake_choices, null=True, blank=True, default='#')
    company = models.CharField(max_length=100, null=True, blank=True, default='#')


    def __str__(self):
        return f"comp: {self.id} - acct: {self.account_number} - agent: {self.agent_id}"
    
class TicketUpdate(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='updates', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/', null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=status_choices, default="In Progress")

    def __str__(self):
        return f"Update for Ticket #{self.ticket.id}"




