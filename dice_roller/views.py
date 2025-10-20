import random
from django.shortcuts import render
from .forms import DiceRollForm

def roll_dice(request):
    results = []
    total = None

    if request.method == 'POST':
        form = DiceRollForm(request.POST)
        if form.is_valid():
            dice = [form.cleaned_data.get(f'die{i}') for i in range(1, 4)]
            dice = [int(d) for d in dice if d]  # filter empty and convert to int
            results = [random.randint(1, d) for d in dice]
            total = sum(results)
    else:
        form = DiceRollForm()

    return render(request, 'dice_roller/roll.html', {
        'form': form,
        'results': results,
        'total': total,
    })
