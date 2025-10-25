from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        full_message = f"New message from BattleRoster contact form:\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject=f"BattleRoster Contact - {name}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["tylerworth.media@gmail.com"],  # your address
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully! We'll get back to you soon.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {e}")

        return redirect("contact")  # redirect to same page (resets form)

    return render(request, "contact.html")

