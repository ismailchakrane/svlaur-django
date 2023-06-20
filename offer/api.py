from rest_framework.decorators import api_view
from django.http import JsonResponse
from .forms import OfferForm
from .models import Offer

@api_view(['POST'])
def offer_create(request):
    data = request.data
    message = 'success'

    form = OfferForm({
        'title': data.get('offerTitle'),
        'created_by': data.get('companyName'),
        'description': data.get('offerDescription'),
        'is_job': data.get('offerType'),
        'offer_img':data.get('offerImg')
    })

    if form.is_valid():
        offer = form.save()
        offer.save()

    else:
        message = form.errors.as_json()

    return JsonResponse({'message': message}, safe=False)
    

