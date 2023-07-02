from django.urls import path

from . import api


urlpatterns = [
    path('create/', api.offer_create, name='offer_create'),
    path('get_internships/', api.get_internships, name='get_internships'),
    path('get_jobs/', api.get_jobs, name='get_jobs'),
    path('<uuid:pk>/', api.get_offer, name='get_offer'),
    path('unverified/<uuid:pk>/', api.get_unverified_offer, name='get_unverified_offer'),
    path('get_offers/', api.get_offers, name='get_offers'),
    path('delete/<uuid:pk>/', api.delete_offer, name='delete_offer'),
    path('verify/<uuid:pk>/', api.verify_offer, name='verify_offer'),

]