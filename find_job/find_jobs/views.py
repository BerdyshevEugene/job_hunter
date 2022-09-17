from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import FindForm
from .models import Specialization, Vacancy


def index(request):
    form = FindForm()
    return render(request, 'find_jobs/index.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    specialization = request.GET.get('specialization')
    page_obj = []
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
    return render(request, 'find_jobs/list.html', {'object_list': page_obj,
                                                    'form': form})
