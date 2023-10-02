from django import forms

class PlayerNameForm(forms.Form):
    player_name = forms.CharField(max_length=20, help_text="Enter your name")

