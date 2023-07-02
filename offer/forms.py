from django.forms import ModelForm

from .models import Offer


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ('title', 'created_by', 'description', 'is_job', 'offer_img', 'offer_pdf',)