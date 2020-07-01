from django.db import models
from django.utils import timezone
from authentication.models import Customer


class Room(models.Model):
    def __str__(self):
        return "{}".format(self.title)

    picture = models.ImageField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=30, unique=True)
    size = models.PositiveIntegerField(default=0)


class Film(models.Model):
    def __str__(self):
        return "{}".format(self.title)

    picture = models.ImageField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=30, unique=True)


class Seance(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booked_sits = models.PositiveIntegerField(default=0) #number of booked sits before selling

    def book_tickets(self, amount):
        self.booked_sits += amount
        return self.save()

    @property
    def left_sits(self):
        return self.room.size - self.booked_sits

    @property
    def conflict_time(self):
        return self.start_time > self.end_time

    @property
    def conflict_time_start(self):
        return self.start_time < timezone.now()


class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, default=object)
    cnt_of_tickets = models.PositiveSmallIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def check_cnt_available(self):
        return self.seance.room.size - self.seance.booked_sits >= self.cnt_of_tickets

    @property
    def money_not_enough(self):
        return self.customer.wallet < self.cnt_of_tickets*self.seance.price

    @property
    def conflict_time_start(self):
        return self.seance.start_time < timezone.now()

    class Meta:
        ordering = ['-create_at']
