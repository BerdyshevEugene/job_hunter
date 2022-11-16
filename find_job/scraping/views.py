from pyexpat import model
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import FindForm, ViewForm
from .models import Vacancy
from django.views.generic import (DetailView, ListView, CreateView,
                                  UpdateView, DeleteView)


def index(request):
    form = FindForm()
    return render(request, 'scraping/index.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    specialization = request.GET.get('specialization')
    context = {'city': city, 'specialization': specialization, 'form': form}
    if city or specialization:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if specialization:
            _filter['specialization__slug'] = specialization

        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)


def view_detail(request, pk):
    queryset = Vacancy.objects.get(pk=pk)
    return render(request, 'scraping/detail.html', {'object': queryset})


class ViewDetail(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'scraping/detail.html'


class ViewList(ListView):
    model = Vacancy
    template_name = 'scraping/list.html'
    form = FindForm()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['specialization'] = self.request.GET.get('specialization')
        context['form'] = self.form

        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        specialization = self.request.GET.get('specialization')
        qs = []
        if city or specialization:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if specialization:
                _filter['specialization__slug'] = specialization
            qs = Vacancy.objects.filter(**_filter).select_related(
                'city',
                'specialization'
            )
        return qs


class ViewCreate(CreateView):
    model = Vacancy
    # fields = '__all__'
    form_class = ViewForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('index')


class ViewUpdate(UpdateView):
    model = Vacancy
    # fields = '__all__'
    form_class = ViewForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('index')


class ViewDelete(DeleteView):
    model = Vacancy
    # template_name = 'scraping/delete.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена')
        return self.post(request, *args, **kwargs)
