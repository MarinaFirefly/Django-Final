from django.db import models
from django.utils import timezone
from authentication.models import Customer
from django.http import HttpResponse
from django.core.validators import MinValueValidator

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


class SeanceManager(models.Manager):
    #class that realises soft delete
    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)

    def deleted(self):
        return super().get_queryset().filter(is_delete=True)


class Seance(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_day = models.DateField()
    end_day = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.00)])
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booked_sits = models.PositiveIntegerField(default=0) #number of booked sits before selling
    is_delete = models.BooleanField(default=False)
    objects = SeanceManager()

    def delete(self, using=None, keep_parents=False):
        if self.booked_sits != 0:
            return HttpResponse("""This amount of tickets isn't available!
            <a href = '..'>Try again</a>
            """)
        self.is_delete = True
        self.save()

    def book_tickets(self, amount):
        self.booked_sits += amount
        return self.save()

    @property
    def left_sits(self):
        return self.room.size - self.booked_sits

    @property
    def conflict_time(self):
        return self.start_day > self.end_day or (self.start_time > self.end_time and self.start_day >= self.end_day)

    @property
    def conflict_time_start(self):
        return self.start_day < timezone.now().date() or (self.start_time < timezone.now().time() and self.start_day <= timezone.now().date())

    class Meta:
        ordering = ['start_day', 'start_time']


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
        return self.seance.start_time < timezone.now().time() and self.seance.start_day <= timezone.now().date()

    class Meta:
        ordering = ['-create_at']
