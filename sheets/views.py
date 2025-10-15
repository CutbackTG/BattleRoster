from django.shortcuts import render, redirect
from django.contrib import messages

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        messages.success(request, "Your message has been sent!")
        return redirect("contact")

    return render(request, "contact.html")
