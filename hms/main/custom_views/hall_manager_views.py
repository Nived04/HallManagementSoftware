from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import uuid
from ..models import *
from ..forms import *


def update_student_hall_dues():
    pass


def update_student_profile(request, stakeholderID):
    client = Client.objects.filter(stakeholderID=stakeholderID)[0]
    student = Student.objects.filter(client=client)[0]
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST, instance=student)
        if form.is_valid():
            client.stakeholderID = form.cleaned_data.get("stakeholderID")
            client.email = form.cleaned_data.get("email")
            client.address = form.cleaned_data.get("address")
            client.mobile = form.cleaned_data.get("mobile")
            client.first_name = form.cleaned_data.get("first_name")
            client.last_name = form.cleaned_data.get("last_name")
            student.hall = form.cleaned_data.get("hall")
            password = form.cleaned_data.get("password")
            client.set_password(password)
            client.save()
            student.client = client
            student.save()
            messages.success(
                request,
                f"Student Profile Edited!",
            )
            return redirect("/hall/search-student")  # Redirect to a success page
    else:
        form = StudentRegistrationForm(
            initial={
                "stakeholderID": stakeholderID,
                "email": client.email,
                "password": client.password,
                "mobile": client.mobile,
                "address": client.address,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "hall": student.hall,
            }
        )
        # print(form.instance)
        # form.instance = student

    return render(request, "hall_manager/update_student_profile.html", {"form": form})


def allot_staff_duties():
    pass


def search_student(request):
    if request.method == "POST":
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            stakeholderID = form.cleaned_data.get("stakeholderID")
            try:
                client = Client.objects.filter(stakeholderID=stakeholderID)[0]
                print(client.role)
                if client.role == "student":
                    return redirect(f"/hall/update-student-profile/{stakeholderID}")
                else:
                    print("popo")
                    messages.MessageFailure(
                        request,
                        f"student not found",
                    )
                    return redirect("/hall/search-student")

            except Student.DoesNotExist:
                messages.MessageFailure(
                    request,
                    f"student not found",
                )
                return redirect("/hall/search-student")
    else:
        form = StudentSearchForm()
    return render(
        request,
        "hall_manager/search_student.html",
        context={"form": form, "title": "register"},
    )


def create_atr(request):
    if request.method == "POST":
        form = ATRForm(request.POST)
        if form.is_valid():
            print(request.POST)
            complaint = form.cleaned_data.get("complaint")
            employee = form.cleaned_data.get("employee")
            report = form.cleaned_data.get("report")
            status = form.cleaned_data.get("status")
            atr = ATR(
                complaint=complaint, employee=employee, report=report, status=status
            )
            atr.save()
            messages.success(
                request,
                f"ATR created!",
            )
            return redirect("hall/complaints")
    else:
        form = ATRForm()
    return render(
        request,
        "hall_manager/create_atr.html",
        context={"form": form, "title": "register"},
    )


def hall_complaints(request):
    if request.method == "GET":
        hall_manager = HallManager.objects.filter(client=request.user)[0]
        complaints = Complaint.objects.filter(hall=hall_manager.hall)
        atrs = []
        for complaint in complaints:
            atr = ATR.objects.filter(complaint=complaint)[0]
            atrs.append(atr)
        print(complaints)
        data = zip(complaints, atrs)
        return render(
            request,
            "hall_manager/complaints.html",
            context={"data": data, "title": "GetComplaints"},
        )


def add_employee(request):
    if request.method == "POST":
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            hall_manager = HallManager.objects.filter(client=request.user)[0]
            stakeholderID = form.cleaned_data.get("stakeholderID")
            email = form.cleaned_data.get("email")
            address = form.cleaned_data.get("address")
            mobile = form.cleaned_data.get("mobile")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = "HallEmployee#123"
            token = str(uuid.uuid4())
            client = Client.objects.create_user(
                stakeholderID,
                email,
                password,
                mobile,
                first_name,
                last_name,
                address,
                token,
                "hall_employee",
            )
            salary = form.cleaned_data.get("salary")
            role = form.cleaned_data.get("role")
            client.is_active = True
            worker = HallEmployee(
                client=client, hall=hall_manager.hall, salary=salary, role=role
            )
            worker.save()
            messages.success(
                request,
                f"Employee {first_name} {last_name} Registered with ID {stakeholderID}",
            )
            return redirect("hall/landing")
    else:
        form = WorkerRegistrationForm()
    return render(
        request,
        "hall_manager/add_employee.html",
        context={"form": form, "title": "register"},
    )


def hall_landing(request):
    return render(request, "hall_manager/landing.html")


def register_student(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            stakeholderID = form.cleaned_data.get("stakeholderID")
            email = form.cleaned_data.get("email")
            address = form.cleaned_data.get("address")
            mobile = form.cleaned_data.get("mobile")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
            hall = form.cleaned_data.get("hall")
            token = str(uuid.uuid4())
            client = Client.objects.create_user(
                stakeholderID,
                email,
                password,
                mobile,
                first_name,
                last_name,
                address,
                token,
                "student",
            )
            student = Student(client=client, hall=hall)
            student.save()
            subject = "Your account needs to be verified"
            message = f"Hi, click on this link to verify your account http://127.0.0.1:8000/hall/verify-student/{token}"
            email_from = "shreya.bose.in@gmail.com"
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(
                request,
                f"Pls click on the link sent to {email} to complete registration",
            )
            return redirect("login")
    else:
        form = StudentRegistrationForm()
    return render(
        request,
        "hall_manager/register_student.html",
        context={"form": form, "title": "register"},
    )


def verify_student(request, token):
    client = Client.objects.filter(token=token).first()
    student = Student.objects.filter(client=client)[0]
    if client:
        client.is_active = True
        client.save()
        passbook = StudentPassbook(student=student)
        passbook.save()
        messages.info(request, "Your account has been verified")
        return redirect("/login")
    else:
        return redirect("/error")