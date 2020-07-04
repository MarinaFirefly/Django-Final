from django import forms
from cinema.models import Film, Purchase, Room, Seance


class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['film', 'start_time', 'end_time', 'start_day', 'end_day', 'price', 'room', 'booked_sits']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['title', 'size']


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['title']


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['cnt_of_tickets', 'seance']


class SearchBoxForm(forms.Form):
    film = forms.CharField()


class SearchBoxFormStart(forms.Form):
    start_day = forms.CharField()


ORDER = (
    ('price', 'By price'),
    ('', 'By start')
)


class OrderingForm(forms.Form):
    order = forms.ChoiceField(choices=ORDER)
