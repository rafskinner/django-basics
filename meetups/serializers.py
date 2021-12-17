from rest_framework import serializers

from meetups.models import Meetup, Location, Participant


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'address']


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant()
        fields = ['email']


class MeetupSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    location = LocationSerializer()
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Meetup
        fields = ['title', 'slug', 'description', 'organizer_email', 'date', 'image', 'location', 'participants']
