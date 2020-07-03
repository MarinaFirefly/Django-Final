from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, DeleteView, TemplateView, View, UpdateView
from cinema.forms import RoomForm, SeanceForm, SearchBoxForm, SearchBoxFormStart, OrderingForm, FilmForm, PurchaseForm
from cinema.models import Film, Purchase, Room, Seance


class SuperuserTestMixin(UserPassesTestMixin):
    # creation of class to differ admin and user
    def test_func(self):
        if self.request.user.is_superuser:
            return True


# CLASSES FOR FETCHING LISTS OF INSTANCES
class RoomsListView(ListView):
    model = Room
    paginate_by = 3
    template_name = 'lists/list_rooms.html'
    queryset = Room.objects.all()
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'room_form': RoomForm,
             })
        return context


class FilmsListView(ListView):
    model = Film
    paginate_by = 3
    template_name = 'lists/list_films.html'
    queryset = Film.objects.all()
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'film_form': FilmForm,
             })
        return context


class SeancesListView(ListView):
    model = Seance
    paginate_by = 5
    template_name = 'index.html'
    queryset = Seance.objects.filter(start_day__gte=timezone.now().date())

    def get_queryset(self):
        search_film = self.request.GET.get('film')
        search_day = self.request.GET.get('start_day')
        order = self.request.GET.get('order')
        if search_film:
            query = Q(film__title__icontains=search_film)
            return self.queryset.filter(query)
        if search_day:
            query = Q(start_day__icontains=search_day)
            return self.queryset.filter(query)
        if order in ['price', 'start_day']:
            return self.queryset.order_by(order)
        else:
            return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'seance_form': SeanceForm,
             'search_form_film': SearchBoxForm,
             'search_form_day': SearchBoxFormStart,
             'ordering_form': OrderingForm,
             'purchase_form': PurchaseForm,
             })
        return context


# CLASSES FOR CREATING INSTANCES
class SeanceCreateView(SuperuserTestMixin, CreateView):
    model = Seance
    template_name = 'creation/create_seance.html'
    form_class = SeanceForm
    success_url = reverse_lazy('create_seance')

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.conflict_time:
            return HttpResponse("""Hey! What's up with seance times??
                <a href = '../create_seance'>Try again</a>
                """)
        if obj.conflict_time_start:
            return HttpResponse("""Seance cannot start in the past
                <a href = '../create_seance'>Try again</a>
                """)
        seances = Seance.objects.filter(room__title=obj.room.title)
        check_all_times = \
            [s for s in seances if (obj.start_day == s.start_day or obj.end_day == s.end_day)
             and (obj.end_time > s.start_time) or obj.start_time < s.end_time]
        if len(check_all_times) != len(seances):
            return HttpResponse("""Seance for this time already exist!
                <a href = '../create_seance'>Try again</a>
                """)
        self.object = obj.save()
        return super().form_valid(form)


class RoomCreateView(SuperuserTestMixin, CreateView):
    model = Room
    template_name = 'creation/create_room.html'
    form_class = RoomForm
    success_url = reverse_lazy('create_room')


class FilmCreateView(SuperuserTestMixin, CreateView):
    model = Film
    template_name = 'creation/create_film.html'
    form_class = FilmForm
    success_url = reverse_lazy('create_film')


# CLASS FOR UPDATING INSTANCES
class FilmUpdateView(SuperuserTestMixin, UpdateView):
    model = Film
    template_name = 'updating/update_film.html'
    success_url = reverse_lazy('list_film')
    fields = ['title']


class RoomUpdateView(SuperuserTestMixin, UpdateView):
    model = Room
    template_name = 'updating/update_room.html'
    success_url = reverse_lazy('list_room')
    fields = ['title', 'size']


class SeanceUpdateView(SuperuserTestMixin, UpdateView):
    model = Seance
    # form_class = UpdateSeanceForm
    template_name = 'updating/update_seance.html'
    success_url = reverse_lazy('index')
    fields = ['start_time', 'end_time', 'price', 'room']

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.conflict_time:
            return HttpResponse("""Hey! What's up with seance times??
                <a href = '../create_seance'>Try again</a>
                """)
        if obj.conflict_time_start:
            return HttpResponse("""Seance cannot start in the past
                <a href = '../..'>Try again</a>
                """)
        seances = Seance.objects.filter(room__title=obj.room.title)
        check_all_times = \
            [s for s in seances if (obj.start_time and obj.end_time < s.start_time) or obj.start_time > s.end_time]
        if len(check_all_times) != len(seances):
            return HttpResponse("""Seance for this time already exist!
                <a href = '../..'>Try again</a>
                """)
        self.object = obj.save()
        return super().form_valid(form)


# CLASS FOR CREATING PURCHASE INSTANCES
class PurchaseCreateView(LoginRequiredMixin, CreateView):
    http_method_names = ['post', ]
    success_url = reverse_lazy('index')
    model = Purchase
    form_class = PurchaseForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.customer = self.request.user
        obj.seance = Seance.objects.get(pk=self.request.POST.get("seance", ""))
        if not obj.check_cnt_available:
            return HttpResponse("""This amount of tickets isn't available!
            <a href = '..'>Try again</a>
            """)
        if obj.money_not_enough:
            return HttpResponse("""You haven't enough money!
            <a href = '..'>Try again</a>
            """)
        if obj.conflict_time_start:
            return HttpResponse("""Hey this seance has already started!
            <a href = '..'>Try again</a>
            """)
        obj.customer.minus_wallet(obj.cnt_of_tickets * obj.seance.price)
        obj.seance.book_tickets(obj.cnt_of_tickets)
        self.object = obj.save()
        return super().form_valid(form)
