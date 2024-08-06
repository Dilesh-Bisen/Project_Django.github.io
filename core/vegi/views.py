from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Student
from django.db.models import Q, Sum
from .seed import generate_reportcard
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


@login_required(login_url="/login")
def recipes(request):
    if request.method == "POST":
        data = request.POST

        recipe_name = data.get("recipe_name")
        recipe_description = data.get("recipe_description")
        recipe_image = request.FILES.get("recipe_image")

        print(recipe_name)
        print(recipe_description)
        print(recipe_image)

        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            recipe_image=recipe_image,
        )

        return redirect("/recipes")

    queryset = Recipe.objects.all()

    if request.GET.get("search_recipe"):
        queryset = queryset.filter(
            recipe_name__icontains=request.GET.get("search_recipe")
        )

    context = {"recipes": queryset, "heading": "Delicious Recipes"}

    return render(request, "recipes.html", context)


@login_required(login_url="/login")
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect("/recipes")


@login_required(login_url="/login")
def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST

        recipe_name = data.get("recipe_name")
        recipe_description = data.get("recipe_description")
        recipe_image = request.FILES.get("recipe_image")

        print(recipe_name)
        print(recipe_description)
        print(recipe_image)

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description
        queryset.recipe_image = recipe_image

        queryset.save()

        return redirect("/recipes")

    context = {"recipes": queryset, "heading": "Update Recipes"}
    return render(request, "update_recipe.html", context)


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already exists.")
            return redirect("/register")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)

        user.save()
        messages.info(request, "Account created successfully.")

        return redirect("/register")

    context = {"heading": "Register Page"}
    return render(request, "register.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(phone_number=username)
        if not user.exists():
            messages.info(request, "Invalid Username.")
            return redirect("/login")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalid Password.")
            return redirect("/login")
        else:
            login(request, user)
            return redirect("/recipes")

    context = {"heading": "Login Page"}
    return render(request, "login.html", context)


def login_out(request):
    logout(request)
    return redirect("/login")


def get_students(request):
    queryset = Student.objects.annotate(
        total_marks=Sum("studentmarks__marks")
    ).order_by("-total_marks")

    if request.GET.get("search"):
        queryset = queryset.filter(
            Q(student_id__student_id__icontains=request.GET.get("search"))
            | Q(department__department__icontains=request.GET.get("search"))
            | Q(student_name__icontains=request.GET.get("search"))
            | Q(student_email__icontains=request.GET.get("search"))
            | Q(student_age__icontains=request.GET.get("search"))
        )

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request, "report/student.html", {"page_obj": page_obj, "heading": "Student"}
    )


def see_marks(request, student_id):
    # generate_reportcard()
    queryset = SubjectMarks.objects.filter(student__student_id__student_id=student_id)

    current_rank = -1
    ranks = Student.objects.annotate(marks=Sum("studentmarks__marks")).order_by(
        "-marks", "-student_age"
    )
    i = 1
    for rank in ranks:
        if student_id == rank.student_id.student_id:
            current_rank = i
            break
        i += 1

    total_marks = queryset.aggregate(total_marks=Sum("marks"))

    context = {
        "queryset": queryset,
        "current_rank": current_rank,
        "total_marks": total_marks,
        "heading": "Report-Card",
    }
    return render(request, "report/see_marks.html", context)
