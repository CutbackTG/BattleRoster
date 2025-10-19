@login_required
def character_update(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)

    if request.method == "POST":
        # Fields to update
        numeric_fields = ["level", "health", "mana", "strength", "dexterity",
                          "constitution", "intelligence", "wisdom", "charisma", "armor_class", "initiative",
                          "fortitude_save", "reflex_save", "will_save"]
        text_fields = ["name", "race", "class_type", "equipment", "weapons", "spells"]

        # Update numeric fields safely
        for field in numeric_fields:
            value = request.POST.get(field)
            setattr(character, field, int(value) if value else 0)

        # Update text fields
        for field in text_fields:
            setattr(character, field, request.POST.get(field, "").strip())

        character.save()
        messages.success(request, f"Character '{character.name}' updated successfully!")
        return redirect("characters")

    return render(request, "character_update.html", {"character": character})
