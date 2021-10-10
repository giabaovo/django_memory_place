from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from memory.models import Memory
from memory.forms import MemoryForm


def index(request):

    if request.user.is_authenticated:
        memories = Memory.objects.filter(owner=request.user)
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
