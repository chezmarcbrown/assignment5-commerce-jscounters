from django import forms


class HackForm(forms.Form):
    listings = forms.IntegerField(initial=0,
                                  label='How many listings should be added or removed?')
    watchlist = forms.IntegerField(initial=0,
                                   label='How many listings on the logged in user should be added or removed from his watchlist?')
