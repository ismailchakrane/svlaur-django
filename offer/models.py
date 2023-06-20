import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings


class Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100,blank=False)
    created_by = models.CharField(max_length=100,blank=False)
    description = models.TextField(blank=False)
    is_job = models.BooleanField(blank=False)
    offer_img = models.ImageField(upload_to='offerimg', blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def get_job_img(self):
        if self.offer_img:
            return settings.WEBSITE_URL + self.offer_img.url
        else:
            return None

    