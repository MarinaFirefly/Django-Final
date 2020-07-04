from rest_framework import serializers
from authentication.models import Customer
from cinema.models import Seance, Purchase, Film


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username']


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class SeanceSerializer(serializers.ModelSerializer):
    film = serializers.CharField(source='film.title')

    class Meta:
        model = Seance
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    seance = SeanceSerializer()
    customer = serializers.CharField(source='customer.username')

    class Meta:
        model = Purchase
        fields = ['id', 'seance', 'cnt_of_tickets', 'customer']
