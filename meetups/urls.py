from django.urls import path

from meetups import views

urlpatterns = [
    path("", views.index, name="all-meetups"),
    path("api/", views.get_meetups, name="get-all-meetups"),
    path("api/<slug:meetup_slug>", views.get_meetup_by_slug, name="get-meetup-by-slug"),
    path("<slug:meetup_slug>/success", views.confirm_registration, name="confirm-registration"),
    path("<slug:meetup_slug>", views.meetup_details, name="meetup-details")
]
