from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm
from django.contrib.auth.hashers import make_password
from .models import User
from django.db.models import Count



@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'last_name': request.user.last_name,
        'first_name': request.user.first_name,
        'email': request.user.email,
        'major': request.user.major,
        'year_of_major': request.user.year_of_major,
        'linkedin_link': request.user.linkedin_link,
        'place_of_work': request.user.place_of_work,
        'job_title': request.user.job_title,
        'year_of_graduate': request.user.year_of_graduate,
        'is_graduate': request.user.is_graduate,
        'is_admin': request.user.is_admin
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    hashed_password = make_password(data.get('password'))

    form = SignupForm({
        'last_name': data.get('lastName'),
        'first_name': data.get('firstName'),
        'email': data.get('email'),
        'password': hashed_password,
        'major':data.get('major'),
        'year_of_major':data.get('yearOfMajor'),
        'linkedin_link':data.get('linkedinLink'),
        'place_of_work':data.get('placeOfWork'),
        'job_title':data.get('jobTitle'),
        'year_of_graduate':data.get('yearOfGraduate'),
        'is_graduate':data.get('isGraduate'),
        'is_admin':data.get('isAdmin')
    })



    if form.is_valid():
        user = form.save()
        user.save()

    else:
        message = form.errors.as_json()
    
    print(message)

    return JsonResponse({'message': message}, safe=False)

@api_view(['GET'])
def get_graduates(request):
    graduates_users = User.objects.filter(is_graduate=True, is_admin=False).order_by('-date_joined')
    
    if len(graduates_users) == 0:
        return JsonResponse(None, safe=False)

    # Convert data to JSON and return as a JSON response
    response_data = []
    for graduate in graduates_users :
        response_data.append({
            'id': graduate.id,
            'last_name': graduate.last_name,
            'first_name': graduate.first_name,
            'email': graduate.email,
            'major': graduate.major,
            'year_of_major': graduate.year_of_major,
            'linkedin_link': graduate.linkedin_link,
            'place_of_work': graduate.place_of_work,
            'job_title': graduate.job_title,
            'year_of_graduate': graduate.year_of_graduate,
        })

    return JsonResponse(response_data, safe=False)


@api_view(['GET'])
def get_users(request):
    users = User.objects.filter(is_admin=False).order_by('-date_joined')

    if len(users) == 0:
        return JsonResponse(None, safe=False)

    # Convert data to JSON and return as a JSON response
    response_data = []
    for user in users :
        response_data.append({
            'id': user.id,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'email': user.email,
            'major': user.major,
            'year_of_major': user.year_of_major,
            'linkedin_link': user.linkedin_link,
            'place_of_work': user.place_of_work,
            'job_title': user.job_title,
            'year_of_graduate': user.year_of_graduate,
        })

    return JsonResponse(response_data, safe=False)

@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        return JsonResponse({'message': 'success'}, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Offer not found'}, status=404, safe=False)
    


@api_view(['GET'])
def get_user(request, pk):
    user = User.objects.get(pk=pk)

    if user is not None:
            return JsonResponse({
                'id': user.id,
                'last_name': user.last_name,
                'first_name': user.first_name,
                'email': user.email,
                'major': user.major,
                'year_of_major': user.year_of_major,
                'linkedin_link': user.linkedin_link,
                'place_of_work': user.place_of_work,
                'job_title': user.job_title,
                'year_of_graduate': user.year_of_graduate,
                'is_graduate' : user.is_graduate,
            }, safe=False)
    
    return JsonResponse(None, safe=False)

@api_view(['PATCH'])
def update_user(request, pk):
    try:

        user = User.objects.get(pk=pk)

        user.last_name = request.data.get('last_name')
        user.first_name = request.data.get('first_name')
        user.email = request.data.get('email')
        user.major = request.data.get('major')
        user.year_of_major = request.data.get('year_of_major')
        user.linkedin_link = request.data.get('linkedin_link')
        user.place_of_work = request.data.get('place_of_work')
        user.job_title = request.data.get('job_title')
        user.year_of_graduate = request.data.get('year_of_graduate')
        user.is_graduate = request.data.get('is_graduate')
        if request.data.get('password') is not None:
            user.password = make_password(request.data.get('password'))
            
        user.save()
        return JsonResponse({'message': 'success'}, safe=False)

    except User.DoesNotExist:
        return JsonResponse({'error': 'Offer not found'}, status=404, safe=False)
    

@api_view(['GET'])
def graduates_per_major(request):
    graduates_per_major = (
        User.objects
        .filter(is_graduate=True,is_admin=False)
        .values('major')
        .annotate(grad_per_major=Count('id'))
        .order_by()
    )


    if len(graduates_per_major) == 0:
        return JsonResponse(None, safe=False)

    majors = []
    for data in graduates_per_major :
        majors.append(data['major'])

    grads_per_major = []
    for data in graduates_per_major :
        grads_per_major.append(data['grad_per_major'])

    response_data = {
        'majors' : majors,
        'grads_per_major' : grads_per_major,
    }

    return JsonResponse(response_data, safe=False)


@api_view(['GET'])
def percentage_of_grad_workers(request):

    has_job_counts = (
        User.objects
        .filter(is_graduate=1, is_admin=0, job_title__isnull=False)
        .aggregate(count=Count('id'))
    )

    no_job_counts = (
        User.objects
        .filter(is_graduate=1, is_admin=0, job_title__isnull=True)
        .aggregate(count=Count('id'))
    )

    total =  int(has_job_counts['count'])  + int(no_job_counts['count']) 
    has_job = (int(has_job_counts['count'])  / total) * 100 if int(has_job_counts['count']) > 0  else 0
    no_job = (int(no_job_counts['count'])  / total ) * 100 if int(no_job_counts['count']) > 0 else 0
    
    print("numbers", has_job, no_job)
    
    response_data = {
        'numbers' : [has_job, no_job],
    }

    return JsonResponse(response_data, safe=False)

