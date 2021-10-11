from django.core import paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.gis.geos import fromstr

from memory.models import Memory


def index(request):

    if request.user.is_authenticated:
        memories_list = Memory.objects.filter(owner=request.user)
        page = request.GET.get('page', 1)

        paginator = Paginator(memories_list, 8)
        try:
            memories = paginator.page(page)
        except PageNotAnInteger:
            memories = paginator.page(1)
        except EmptyPage:
            memories = paginator.page(paginator.num_pages)
        context = {
            'memories': memories,
        }
        return render(request, 'index.html', context)

    return render(request, 'index.html')


@login_required
def memory_detail(request, pk):
    m = Memory.objects.filter(owner=request.user)
    memory = get_object_or_404(m, pk=pk)

    context = {
        'memory': memory,
    }

    return render(request, 'memory/detail.html', context)


@login_required
def memory_add(request):
    if request.method == 'POST':
        owner = request.user
        name = request.POST.get('memory_name')
        description = request.POST.get('memory_des')
        my_long = request.POST.get('lng')
        my_lat = request.POST.get('lat')
        my_long_lat = my_long + " " + my_lat
        location = fromstr('POINT(' + my_long_lat + ')')

        memory = Memory.objects.create(
            name=name, owner=owner, descripsion=description, location=location)
        memory.save()
        return redirect('/')
    return render(request, 'memory/add.html')


@login_required
def memory_data(request):

    memories = serialize('geojson', Memory.objects.filter(owner=request.user))
    return HttpResponse(memories, content_type='json')
