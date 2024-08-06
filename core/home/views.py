from django.shortcuts import render, redirect
from django.http import HttpResponse
from vegi.seed import *
from .utils import send_email_with_attachment
# from .utils import send_email_to_client
from django.conf import settings
from home.models import Car
import random
# Create your views here.
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(request):
    subject = "This mail is from Django Server"
    message = "This is a attach file with this email hosted by Dilesh Bisen"
    recipient_list = []
    for i in os.getenv('EMAIL').split():
        recipient_list.append(i)
    file_path = f"{settings.BASE_DIR}/fees.png"
    # send_email_to_client()
    print(os.getenv('EMAIL'))
    send_email_with_attachment(subject, message, recipient_list, file_path)
    return redirect("/")


# def home(request):
#     return HttpResponse("""
#         <h1>This is a Django Server.</h1>
#         <p>Hey this is coming from Django server.</p>
#         """)
def home(request):
    # seed_db(100)
    Car.objects.create(car_name="Rolls Royce")

    peoples = [
        {"name": "Dilesh", "age": 20},
        {"name": "Vijay", "age": 19},
        {"name": "Jay", "age": 10},
        {"name": "Raju", "age": 26},
        {"name": "Ajay", "age": 15},
        {"name": "Prakash", "age": 8},
    ]

    text = "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Atque illum odit ratione molestias pariatur fugiat eum temporibus assumenda dolorum, a eos, excepturi vero perferendis soluta, odio fugit cumque. Ab, quibusdam!"

    return render(
        request,
        "home/index.html",
        context={"heading": "Django Server", "peoples": peoples, "text": text},
    )


def about(request):
    context = {"heading": "About"}
    return render(request, "home/about.html", context)


def contact(request):
    context = {"heading": "Contact"}
    return render(request, "home/contact.html", context)


def success_page(request):
    print("#" * 10)
    return HttpResponse("<h1>Hey this is a Success Page.</h1>")
