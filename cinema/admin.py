from django.contrib import admin

from cinema.models import Customer, Room, Seance, Purchase, Film

admin.site.register(Customer)
admin.site.register(Room)
admin.site.register(Seance)
admin.site.register(Purchase)
admin.site.register(Film)
