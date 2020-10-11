from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator
from django.urls import reverse

from .forms import SummonerLeagueForm, SummonerForm, HistoryForm
from .models import Summoner, SummonerHistory
from sync.client import get_summoner_by_name


def leagues(request, region=None):
    if region is None:
        # Maybe add ip geolocation here
        region = 'eun1'

    defaults = {
        'region': region,
        'queue': 'RANKED_SOLO_5x5',
        'tier': 'CHALLENGER',
        'division': 'I',
    }
    form = SummonerLeagueForm(request.GET or defaults)
    summoner_form = SummonerForm(initial={
                                 'region': (request.GET.get(
                                        'region') or region)})
    if form.is_valid():
        data = form.get_data()
        paginator = Paginator(data, 20)
        page_number = request.GET.get('page')
        results = paginator.get_page(page_number)
    else:
        results = []

    context = {
        'results': results,
        'form': form,
        'summoner_form': summoner_form,
        'region': defaults['region']
    }
    return render(request, 'summoners/leagues.html', context)


def profile(request, id):
    try:
        summoner = get_object_or_404(Summoner, id=id)
    except Http404:
        return redirect(reverse('leagues'))
    history_form = HistoryForm(request.GET or None)
    if history_form.is_valid():
        data = history_form.get_data(summoner=summoner)
    else:
        data = SummonerHistory.objects.filter(summoner=summoner,
                                              queue='RANKED_SOLO_5x5').all()
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    history = paginator.get_page(page_number)
    summoner_form = SummonerForm()
    context = {
        'summoner': summoner,
        'summoner_form': summoner_form,
        'history_form': history_form,
        'history': history,
    }
    return render(request, 'summoners/profile.html', context)


def update(request, id):
    try:
        old_summoner = get_object_or_404(Summoner, id=id)
    except Http404:
        return redirect(reverse('leagues'))
    summoner = get_summoner_by_name(name=old_summoner.name,
                                    region_name=old_summoner.region.name)
    if summoner is None:
        return redirect(reverse('profile', kwargs={'id': old_summoner.id}))
    return redirect(reverse('profile', kwargs={'id': summoner.id}))


def search(request):
    form = SummonerForm(request.GET)
    if form.is_valid():
        name = request.GET.get('name')
        region_name = request.GET.get('region')
        if len(name) == 0:
            return redirect(reverse('leagues_by_region',
                                    kwargs={'region': region_name}))
        summoner = form.get_data()
        if not summoner.exists():
            summoner = get_summoner_by_name(name=name,
                                            region_name=region_name)
        else:
            summoner = summoner.get()
        return redirect(reverse('profile', kwargs={'id': summoner.id}))
    else:
        return redirect(reverse('leagues'))
