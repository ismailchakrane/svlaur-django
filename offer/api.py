
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from .forms import OfferForm
from .models import Offer


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def offer_create(request):
    message = 'success'
    
    form = OfferForm(request.POST, request.FILES)

    if form.is_valid():
        offer = form.save()
        offer.save()

    else:
        message = form.errors.as_json()

    return JsonResponse({'message': message}, safe=False)

@api_view(['GET'])
def get_internships(request):
    internships = Offer.objects.filter(is_verified=True, is_job=False).order_by('-date_created')

    if len(internships) == 0:
        return JsonResponse(None, safe=False)

    response_data = []
    for internship in internships :
        response_data.append({
            'id': internship.id,
            'title': internship.title,
            'created_by': internship.created_by,
            'description': internship.description,
            'date_created': internship.date_created,                
        })

    # title = models.CharField(max_length=100,blank=False)
    # created_by = models.CharField(max_length=100,blank=False)
    # description = models.TextField(blank=False)
    # is_job = models.BooleanField(blank=False)
    # offer_img = models.ImageField(upload_to='offerimgs', blank=True, null=True)
    # offer_pdf = models.FileField(upload_to='offerpdfs', blank=True, null=True)
    # is_verified = models.BooleanField(default=False)
    # date_created = models.DateTimeField(default=timezone.now)
    
    return JsonResponse(response_data, safe=False)

@api_view(['GET'])
def get_jobs(request):
    jobs = Offer.objects.filter(is_verified=True, is_job=True).order_by('-date_created')

    if len(jobs) == 0:
        return JsonResponse(None, safe=False)
    
    response_data = []
    for job in jobs :
        response_data.append({
            'id': job.id,
            'title': job.title,
            'created_by': job.created_by,
            'description': job.description,
            'date_created': job.date_created,                
        })
    
    return JsonResponse(response_data, safe=False)

@api_view(['GET'])
def get_offer(request, pk):
    offer = Offer.objects.get(pk=pk)

    if offer is not None:
            return JsonResponse({
                'title': offer.title,
                'created_by': offer.created_by,
                'description': offer.description,
                'date_created': offer.date_created,
                'offer_img': offer.get_job_img(),
                'offer_pdf': offer.get_job_pdf()
            }, safe=False)
    
    return JsonResponse(None, safe=False)

@api_view(['GET'])
def get_offers(request):
    offers = Offer.objects.filter(is_verified=False).order_by('-date_created')

    if len(offers) == 0:
        return JsonResponse(None, safe=False)
    
    response_data = []
    for offer in offers :
        response_data.append({
            'id': offer.id,
            'title': offer.title,
            'created_by': offer.created_by,
            'description': offer.description,
            'date_created': offer.date_created,                
        })
    
    return JsonResponse(response_data, safe=False)

@api_view(['GET'])
def get_unverified_offer(request, pk):
    offer = Offer.objects.get(pk=pk)

    if offer is not None and offer.is_verified is False:
            return JsonResponse({
                'title': offer.title,
                'created_by': offer.created_by,
                'description': offer.description,
                'date_created': offer.date_created,
                'offer_img': offer.get_job_img(),
                'offer_pdf': offer.get_job_pdf()
            }, safe=False)
    
    return JsonResponse(None, safe=False)

@api_view(['DELETE'])
def delete_offer(request, pk):
    try:
        offer = Offer.objects.get(pk=pk)
        offer.delete()
        return JsonResponse({'message': 'success'}, safe=False)
    except Offer.DoesNotExist:
        return JsonResponse({'error': 'Offer not found'}, status=404, safe=False)
    
@api_view(['PATCH'])
def verify_offer(request, pk):
    try:
        offer = Offer.objects.get(pk=pk)
        offer.is_verified = True
        offer.save()
        return JsonResponse({'message': 'success'}, safe=False)
    except Offer.DoesNotExist:
        return JsonResponse({'error': 'Offer not found'}, status=404, safe=False)
