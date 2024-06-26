from django import forms
from .models import *
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
import re


class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            "stakeholderID",
            "email",
            "password",
            "mobile",
            "address",
            "role",
            "first_name",
            "last_name",
        )


class StudentRegistrationForm(forms.ModelForm):

    stakeholderID = forms.CharField(max_length=50)
    email = forms.EmailField(empty_value=None)
    password = forms.CharField(empty_value=None, max_length=400)
    mobile = PhoneNumberField()
    address = forms.CharField(widget=forms.Textarea)
    first_name = forms.CharField(max_length=150, empty_value=None)
    last_name = forms.CharField(max_length=150, empty_value=None)
    room_choice1 = forms.CharField(
        label="Room First Choice",
        max_length=4,
        empty_value=None,
    )
    room_choice2 = forms.CharField(
        label="Room Second Choice",
        max_length=4,
        empty_value=None,
    )
    room_choice3 = forms.CharField(
        label="Room Third Choice",
        max_length=4,
        empty_value=None,
    )

    class Meta:
        model = Student
        fields = (
            "stakeholderID",
            "email",
            "password",
            "mobile",
            "address",
            "first_name",
            "last_name",
            "room_choice1",
            "room_choice2",
            "room_choice3",
            "hall",
        )


class StudentSearchForm(forms.Form):
    stakeholderID = forms.CharField(label="Student ID", max_length=50)


class ManagerRegistrationForm(forms.ModelForm):
    stakeholderID = forms.CharField(max_length=50)
    email = forms.EmailField(empty_value=None)
    password = forms.CharField(empty_value=None, max_length=400)
    mobile = PhoneNumberField()
    address = forms.CharField(widget=forms.Textarea)
    first_name = forms.CharField(max_length=150, empty_value=None)
    last_name = forms.CharField(max_length=150, empty_value=None)

    class Meta:
        model = HallManager
        fields = (
            "stakeholderID",
            "email",
            "password",
            "mobile",
            "address",
            "first_name",
            "last_name",
        )


class WardenRegistrationForm(forms.ModelForm):
    stakeholderID = forms.CharField(max_length=50)
    email = forms.EmailField(empty_value=None)
    password = forms.CharField(empty_value=None, max_length=400)
    mobile = PhoneNumberField()
    address = forms.CharField(widget=forms.Textarea)
    first_name = forms.CharField(max_length=150, empty_value=None)
    last_name = forms.CharField(max_length=150, empty_value=None)

    class Meta:
        model = Warden
        fields = (
            "stakeholderID",
            "email",
            "password",
            "mobile",
            "address",
            "first_name",
            "last_name",
            "hall",
            "department",
            "designation",
            "posts_held",
        )


class WorkerRegistrationForm(forms.ModelForm):
    stakeholderID = forms.CharField(max_length=50)
    email = forms.EmailField(empty_value=None)
    mobile = PhoneNumberField()
    address = forms.CharField(widget=forms.Textarea)
    first_name = forms.CharField(max_length=150, empty_value=None)
    last_name = forms.CharField(max_length=150, empty_value=None)

    class Meta:
        model = HallEmployee
        fields = (
            "stakeholderID",
            "email",
            "mobile",
            "address",
            "first_name",
            "last_name",
            "salary",
            "role",
        )


class ATRForm(forms.ModelForm):
    class Meta:
        model = ATR
        fields = (
            "complaint",
            "status",
            "employee",
            "report",
        )


class AllotmentForm(forms.Form):
    hall_allotment = forms.DecimalField(
        label="Hall Allotment",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    mess_allotment = forms.DecimalField(
        label="Mess Allotment",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    verify_password = forms.CharField(
        label="Confirm Password", max_length=100, widget=forms.PasswordInput()
    )


class GrantForm(forms.Form):
    hall = forms.ModelChoiceField(
        queryset=Hall.objects.all(),
        to_field_name="name",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    amount = forms.DecimalField(
        label="Amount",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    verify_password = forms.CharField(
        label="Confirm Password", max_length=100, widget=forms.PasswordInput()
    )


class LeaveForm(forms.Form):
    stakeholderID = forms.CharField(
        label="EmployeeID",
        max_length=20,
    )
    leave_from = forms.DateField(label="Leave from")
    leave_upto = forms.DateField(label="Leave upto")
    reason = forms.CharField(label="Reason")
    uploads = forms.FileField()


class NoticeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = (
            "title",
            "content",
            "image",
        )


class ComplaintRegistrationForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ("title", "content", "category", "image")


class HallRegistrationForm(forms.ModelForm):
    rent_singles = forms.DecimalField(
        label="Rent for Single Rooms",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    rent_doubles = forms.DecimalField(
        label="Rent for Double Rooms",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    rent_triples = forms.DecimalField(
        label="Rent for Triple Rooms",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        model = Hall
        fields = (
            "name",
            "blocks",
            "floors",
            "singles",
            "rent_singles",
            "doubles",
            "rent_doubles",
            "triples",
            "rent_triples",
        )


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ("hall",)


class PaymentForm(forms.Form):
    amount = forms.DecimalField(
        label="Amount",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )

    def __init__(self, total_due, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amount"].validators.append(MaxValueValidator(total_due))
        self.fields["amount"].initial = total_due


class RationForm(forms.ModelForm):
    class Meta:
        model = Ration
        exclude = ("hall", "total")


class VerifyForm(forms.Form):
    amount = forms.DecimalField(
        label="Amount",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    verify_password = forms.CharField(
        label="Confirm Password", max_length=100, widget=forms.PasswordInput()
    )


class ConfirmForm(forms.Form):
    verify_password = forms.CharField(
        label="Confirm Password", max_length=100, widget=forms.PasswordInput()
    )

class DeleteUserForm(forms.Form):
    stakeholderID = forms.CharField(
        label="StakeholderID",
        max_length=50,
    )
    verify_password = forms.CharField(
        label="Confirm Password", max_length=100, widget=forms.PasswordInput()
    )