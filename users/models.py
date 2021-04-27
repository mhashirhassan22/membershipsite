from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
import uuid
# # Create your models here.


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    member_id = models.CharField(max_length=10, null=False, blank=True)
    work_title = models.CharField(max_length=50, null=True, blank=True)
    credit_card = models.CharField(max_length=30, null=True, blank=True)
    business_name = models.CharField(max_length=256, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    is_business = models.BooleanField(default=False)
    phone = models.CharField(max_length=60, null=True, blank=True)
    country = models.CharField(max_length=60, null=True, blank=True)
    state = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=60, null=True, blank=True)
    timezone = models.CharField(max_length=60, null=True, blank=True)

    
    def __str__(self):
        return self.username



class ServiceArea(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)

if(ServiceArea.objects.count()<5):
    t = ServiceArea.objects.create(name="Global")
    t = ServiceArea.objects.create(name="Asia-Pacific")
    t = ServiceArea.objects.create(name="China")
    t = ServiceArea.objects.create(name="India")
    t = ServiceArea.objects.create(name="Europe")
    t = ServiceArea.objects.create(name="Latin America")
    t = ServiceArea.objects.create(name="Middle East & Africa")
    t = ServiceArea.objects.create(name="USA/Canada")


class Interest(models.Model):
    name = models.CharField(max_length=300, unique=True, blank=False, null=False)


if(Interest.objects.count()<23):
    t = Interest.objects.create(name="Agency management")
    t = Interest.objects.create(name="Resource and capabilities")
    t = Interest.objects.create(name="Brand (incl. brand safety)")
    t = Interest.objects.create(name="Social (incl. influencer)")
    t = Interest.objects.create(name="Content and creative production")
    t = Interest.objects.create(name="Sustainability")
    t = Interest.objects.create(name="Data and technology")
    t = Interest.objects.create(name="Transformation")
    t = Interest.objects.create(name="Diversity and Inclusion")
    t = Interest.objects.create(name="Emerging trends")
    t = Interest.objects.create(name="Advertising standards / self-regulation")
    t = Interest.objects.create(name="Evolution of marketing procurement")
    t = Interest.objects.create(name="Alcohol marketing policy")
    t = Interest.objects.create(name="Innovation")
    t = Interest.objects.create(name="Digital policy")
    t = Interest.objects.create(name="Marcomms planning")
    t = Interest.objects.create(name="Food marketing policy")
    t = Interest.objects.create(name="Measurement and effectiveness")
    t = Interest.objects.create(name="Marketing Law")
    t = Interest.objects.create(name="Media buying (incl. programmatic)")
    t = Interest.objects.create(name="Marketing to children")
    t = Interest.objects.create(name="Partnerships and sponsorship")
    t = Interest.objects.create(name="Privacy")
    t = Interest.objects.create(name="Research and consumer insights")
    

class UserInterest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )
    interest = models.ForeignKey(
        Interest,
        on_delete=models.PROTECT,
        related_name='interests'
    )

