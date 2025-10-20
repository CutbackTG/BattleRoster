from django import forms

DICE_CHOICES = [
    (3, 'D3'),
    (4, 'D4'),
    (6, 'D6'),
    (7, 'D7'),
    (8, 'D8'),
    (10, 'D10'),
    (12, 'D12'),
    (20, 'D20'),
]

class DiceRollForm(forms.Form):
    die1 = forms.ChoiceField(choices=DICE_CHOICES, required=False)
    die2 = forms.ChoiceField(choices=DICE_CHOICES, required=False)
    die3 = forms.ChoiceField(choices=DICE_CHOICES, required=False)
