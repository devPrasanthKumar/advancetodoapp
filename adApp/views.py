from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, FormView, ListView, UpdateView, DeleteView
from .models import ListDetails, CustomUser
from .forms import FormForListDetails, LoginForm, UserEditForm
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

# authenticatioon model
from .forms import SignInForm, LoginForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.contrib.auth import login,  authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


# index view
class addView(LoginRequiredMixin, CreateView, FormView,):
    template_name = 'add.html'
    login_url = "login"
    model = ListDetails
    form_class = FormForListDetails

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        messages.success(self.request, "Added succusfully")
        return redirect(reverse("show"))


class ShowData(LoginRequiredMixin, ListView):
    model = ListDetails
    login_url = "login"
    template_name = "index.html"
    context_object_name = "showdetails"

    def get_queryset(self):
        user = self.request.user
        specificData = ListDetails.objects.none()

        if user.is_authenticated:
            specificData = ListDetails.objects.filter(owner=user)
            return specificData

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        pendigTask = ListDetails.objects.filter(
            is_finished=False, owner=self.request.user).count()
        finishedTask = ListDetails.objects.filter(
            is_finished=True, owner=self.request.user).count()
        context["pendingTask"] = pendigTask
        context["finishedTask"] = finishedTask

        return context

# update


class UpdateDetails(LoginRequiredMixin, UpdateView):
    model = ListDetails
    form_class = FormForListDetails
    template_name = "add.html"
    context_object_name = "showD"
    login_url = "login"

    def form_valid(self, form):
        instance = self.get_object()
        instance.save()

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the 'show' page after successful update
        messages.success(self.request, "Updated Successfully ")
        return reverse("show")


class DeleteDetails(LoginRequiredMixin, DeleteView):
    model = ListDetails
    template_name = "confirm_delete.html"
    context_object_name = "showdetails"
    success_url = reverse_lazy('show')
    login_url = "login"


def sort_list(request, showType):
    getFilterData = request.POST.get("sortList")
    orderData = ListDetails.objects.all()
    if getFilterData == "completed":
        orderData = ListDetails.objects.filter(is_finished=True)
        return render(request, "index.html", {"showdetails": orderData})
    elif getFilterData == "pending":
        orderData = ListDetails.objects.filter(is_finished=False)
        return render(request, "index.html", {"showdetails": orderData})
    else:
        orderData = ListDetails.objects.all()
        return render(request, "index.html", {"showdetails": orderData})

# authentication


class SignInView(FormView):
    model = CustomUser
    form_class = SignInForm
    template_name = "sign.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Account Created SuccessFully")
        return redirect("login")


class LoginView(FormView):
    model = User
    form_class = LoginForm
    template_name = "login.html"

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        authuser = authenticate(username=username, password=password)

        if authuser is not None:

            login(self.request, authuser)
            messages.success(self.request, "Login Successfully ")

            print(self.request.user.is_staff)
            return redirect("show")
        else:
            form.add_error(None, "Invalid creadentials")
            return super().form_invalid(form)


class UserProfile(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "user_profile.html"


class UserSettings(LoginRequiredMixin, UpdateView):
    model = CustomUser
    login_url = "login"
    template_name = "user_settings.html"
    success_url = reverse_lazy("show")
    form_class = UserEditForm

    def get_object(self, **kwargs):
        token = self.kwargs.get("uuid")
        print(token)
        return get_object_or_404(CustomUser, uuid=token)

    def get_success_url(self):
        return reverse("user-profile")


class CustomChangePassword(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    login_url = "login"
    template_name = "change_password.html"
    success_url = reverse_lazy("show")
