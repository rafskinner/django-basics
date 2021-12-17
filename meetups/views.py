from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from meetups.forms import RegistrationForm
from meetups.models import Meetup, Participant
from meetups.serializers import MeetupSerializer


def index(req):
    # meetups = [
    #     {"title": "1st meetup", "location": "NY", "slug": "1st-meetup"},
    #     {"title": "2nd meetup", "location": "Paris", "slug": "2nd-meetup"}
    # ]
    meetups = Meetup.objects.all()
    return render(req, 'meetups/index.html', {"meetups": meetups})


def meetup_details(req, meetup_slug):
    try:
        selected_meetup = Meetup.objects.get(slug=meetup_slug)
        if req.method == 'GET':
            registration_form = RegistrationForm()
        else:
            registration_form = RegistrationForm(req.POST)
            if registration_form.is_valid():
                participant_email = registration_form.cleaned_data["email"]
                participant, _ = Participant.objects.get_or_create(email=participant_email)
                selected_meetup.participants.add(participant)
                return redirect('confirm-registration', meetup_slug=meetup_slug)

        return render(req, 'meetups/meetup-details.html',
                      {"meetup": selected_meetup,
                       "meetup_found": True,
                       "form": registration_form
                       })
    except Exception as e:
        return render(req, 'meetups/meetup-details.html', {"meetup_found": False})


def confirm_registration(req, meetup_slug):
    meetup = Meetup.objects.get(slug=meetup_slug)
    return render(req, 'meetups/registration-success.html', {"meetup": meetup})


@api_view(["GET", "POST"])
def get_meetups(req):
    try:
        if req.method == "GET":
            meetups = Meetup.objects.all()
            serializer = MeetupSerializer(meetups, many=True)
            return Response(serializer.data)
        else:
            serializer = MeetupSerializer(data=req.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "PUT", "DELETE"])
def get_meetup_by_slug(req, meetup_slug):
    try:
        meetup = Meetup.objects.get(slug=meetup_slug)
        if req.method == "GET":
            serializer = MeetupSerializer(meetup)
            return Response(serializer.data)
        elif req.method == "PUT":
            serializer = MeetupSerializer(meetup, data=req.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            meetup.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)
