from django import forms

from lol import settings

from .models import SummonerLeague, Summoner, SummonerHistory


class SummonerLeagueForm(forms.ModelForm):
    class Meta:
        model = SummonerLeague
        fields = [
            'queue',
            'tier',
            'division',
        ]

    region = forms.ChoiceField(choices=settings.REGIONS,
                               required=True, initial='eun1')

    def __init__(self, *args, **kwargs):
        super(SummonerLeagueForm, self).__init__(*args, **kwargs)
        self.fields['queue'].required = True
        self.fields['queue'].initial = 'CHALLENGER'
        self.fields['tier'].required = True
        self.fields['tier'].initial = 'RANKED_SOLO_5x5'
        self.fields['division'].required = True
        self.fields['division'].initial = 'I'

    def get_data(self):
        params = self.cleaned_data
        region = params.pop('region')
        data = SummonerLeague.objects.all(
            ).filter(summoner__region__name=region, **params)
        return data


class SummonerForm(forms.ModelForm):
    class Meta:
        model = Summoner
        fields = [
            'name',
        ]

    region = forms.ChoiceField(choices=settings.REGIONS,
                               required=True, initial='eun1',
                               widget=forms.Select(attrs={'onchange': 'document.getElementById("sform").submit();'}))

    def __init__(self, *args, **kwargs):
        super(SummonerForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['name'].initial = ''

    def get_data(self):
        params = self.cleaned_data
        region = params.pop('region')
        name = params.pop('name')
        data = Summoner.objects.all(
            ).filter(region__name=region, name__iexact=name)
        return data


class HistoryForm(forms.ModelForm):
    class Meta:
        model = SummonerHistory
        fields = [
            'queue',
            'champion',
        ]

    def __init__(self, *args, **kwargs):
        super(HistoryForm, self).__init__(*args, **kwargs)
        self.fields['champion'].widget = forms.TextInput()
        self.fields['champion'].required = False
        self.fields['champion'].initial = ''
        self.fields['queue'].widget = forms.Select(
                        choices=settings.QUEUES, attrs={
                'onchange': 'document.getElementById("hform").submit();'})
        self.fields['queue'].initial = 'RANKED_SOLO_5x5'

    def get_data(self, summoner):
        # WIP till I get champions data
        params = self.cleaned_data
        champion = params.pop('champion')
        queue = params.pop('queue')
        data = SummonerHistory.objects.all(
            ).filter(summoner=summoner, queue=queue)
        return data
        '''
         data = SummonerHistory.objects.all(
            ).filter(summoner=id, champion__iexact=champion, queue=queue)
        return data
        '''
