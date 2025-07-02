from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="category_freelancers")
    bio = models.CharField(max_length=256, null=True, blank=True)

class Job(models.Model):
    job_title = models.CharField(max_length=32)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listed_job")
    freelancer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="working_job")
    reward = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="category_job")
    description = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    file = models.FileField(upload_to='main_app/static/uploads', default="", null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} by {self.client}"


class Notification(models.Model):
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification")
    message = models.CharField(max_length=128)
    job =  models.ForeignKey(Job, on_delete=models.CASCADE, related_name="notification", default='')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"to: {self.to}, {self.message}"


class RequestToClient(models.Model):
    freelancer = models.ForeignKey(User, on_delete = models.CASCADE, related_name="sent_request_to_client")
    client = models.ForeignKey(User, on_delete = models.CASCADE, related_name="received_request_from_freelancer")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="request_to_client")

    def __str__(self):
        return f"From Freelancer: {self.freelancer} to Client: {self.client}"