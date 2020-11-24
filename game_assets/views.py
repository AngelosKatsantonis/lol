from django.shortcuts import render, redirect
from django.urls import reverse


from .models import Champion


def champions(request):
    champions = Champion.objects.filter()
    context = {
        'champions': champions,
    }
    return render(request, 'champions/champions.html', context)


def champion_by_name(request, name=None):
    if name is not None:
        champion = Champion.objects.filter(name__iexact=name)
        if champion.exists():
            print(champion.get().get_passive())
            context = {
                'champion': champion.get(),
            }
            return render(request, 'champions/champion.html', context)
    return redirect(reverse('champions'))
