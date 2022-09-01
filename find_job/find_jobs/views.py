from django.shortcuts import render

from .forms import FindForm
from .models import Specialization, Vacancy


def index(request):
    form = FindForm()
    city = request.GET.get('city')
    specialization = request.GET.get('specialization')
    qs = []
    if city or specialization:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if specialization:
            _filter['specialization__slug'] = specialization

        qs = Vacancy.objects.filter(**_filter)
    return render(request, 'find_jobs/index.html', {'object_list': qs,
                                                    'form': form})
